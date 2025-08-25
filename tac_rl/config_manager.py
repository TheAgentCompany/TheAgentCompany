"""
Configuration Management for TAC-RL
===================================

Handles loading, validation, and management of training configurations.
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from dataclasses import dataclass

from .architecture import TrainingConfig, ModelConfig, TaskDomain, TrainingPhase

class ConfigManager:
    """Manages training configuration loading and validation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_cache = {}
    
    def load_config(self, config_path: str) -> TrainingConfig:
        """Load configuration from YAML file"""
        
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            self.logger.info(f"Loaded configuration from {config_path}")
            
            # Parse and validate configuration
            training_config = self._parse_config(config_data)
            
            # Cache for later use
            self.config_cache[str(config_path)] = training_config
            
            return training_config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise
    
    def _parse_config(self, config_data: Dict[str, Any]) -> TrainingConfig:
        """Parse configuration data into TrainingConfig object"""
        
        # Parse model configuration
        model_data = config_data.get('model', {})
        model_config = ModelConfig(
            name=model_data.get('name', 'unknown-model'),
            base_model_path=model_data.get('base_model_path', ''),
            model_type=model_data.get('model_type', 'unknown'),
            parameter_count=model_data.get('parameter_count', 'unknown'),
            context_length=model_data.get('context_length', 4096),
            supports_function_calling=model_data.get('supports_function_calling', False)
        )
        
        # Parse training configuration
        training_data = config_data.get('training', {})
        
        # Parse current phase
        current_phase_str = training_data.get('current_phase', 'warmup')
        try:
            current_phase = TrainingPhase(current_phase_str)
        except ValueError:
            self.logger.warning(f"Invalid phase '{current_phase_str}', using warmup")
            current_phase = TrainingPhase.WARMUP
        
        # Create training configuration
        training_config = TrainingConfig(
            model=model_config,
            algorithm=training_data.get('algorithm', 'grpo'),
            batch_size=training_data.get('batch_size', 8),
            learning_rate=float(training_data.get('learning_rate', 1e-5)),
            max_episodes_per_task=training_data.get('max_episodes_per_task', 3),
            reward_scale=float(training_data.get('reward_scale', 1.0)),
            current_phase=current_phase,
            tasks_per_phase=training_data.get('tasks_per_phase', 20),
            success_threshold=float(training_data.get('success_threshold', 0.7)),
            max_parallel_tasks=training_data.get('max_parallel_tasks', 4),
            checkpoint_frequency=training_data.get('checkpoint_frequency', 100),
            evaluation_frequency=training_data.get('evaluation_frequency', 50),
            output_dir=training_data.get('output_dir', './outputs'),
            checkpoint_dir=training_data.get('checkpoint_dir', './checkpoints'),
            log_dir=training_data.get('log_dir', './logs')
        )
        
        # Add additional configuration sections
        self._parse_additional_config(training_config, config_data)
        
        # Validate configuration
        self._validate_config(training_config)
        
        return training_config
    
    def _parse_additional_config(self, config: TrainingConfig, config_data: Dict[str, Any]):
        """Parse additional configuration sections"""
        
        # Add monitoring configuration
        if not hasattr(config, 'monitoring'):
            config.monitoring = config_data.get('monitoring', {
                'use_wandb': False,
                'project_name': 'tac-rl-training',
                'log_level': 'INFO',
                'save_trajectories': True,
                'realtime_monitoring': True
            })
        
        # Add OpenHands configuration
        if not hasattr(config, 'openhands'):
            config.openhands = config_data.get('openhands', {
                'max_iterations': 100,
                'timeout': 300,
                'enable_auto_lint': True,
                'use_host_network': True
            })
        
        # Add environment configuration
        if not hasattr(config, 'environment'):
            config.environment = config_data.get('environment', {
                'server_hostname': 'localhost',
                'services': ['gitlab', 'plane', 'rocketchat', 'owncloud', 'api-server']
            })
        
        # Add task phase configuration
        if not hasattr(config, 'task_phases'):
            config.task_phases = config_data.get('task_phases', {
                'warmup': ['admin-make-spreadsheet', 'hr-check-attendance-one-day'],
                'intermediate': ['admin-arrange-meeting-rooms', 'hr-check-attendance-multiple-days'],
                'advanced': ['pm-create-plane-issue', 'admin-employee-info-reconciliation'],
                'expert': []  # All remaining tasks
            })
    
    def _validate_config(self, config: TrainingConfig):
        """Validate configuration values"""
        
        errors = []
        
        # Model validation
        if not config.model.base_model_path:
            errors.append("Model base_model_path is required")
        
        if config.model.context_length <= 0:
            errors.append("Model context_length must be positive")
        
        # Training validation
        if config.batch_size <= 0:
            errors.append("Batch size must be positive")
        
        if config.learning_rate <= 0 or config.learning_rate > 1:
            errors.append("Learning rate must be between 0 and 1")
        
        if config.reward_scale <= 0:
            errors.append("Reward scale must be positive")
        
        if config.success_threshold < 0 or config.success_threshold > 1:
            errors.append("Success threshold must be between 0 and 1")
        
        # Path validation
        required_paths = ['output_dir', 'checkpoint_dir', 'log_dir']
        for path_name in required_paths:
            path = getattr(config, path_name)
            if not path:
                errors.append(f"{path_name} is required")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
            raise ValueError(error_msg)
        
        self.logger.info("Configuration validation passed")
    
    def create_default_config(self, model_name: str = "qwen-2.5-7b") -> Dict[str, Any]:
        """Create a default configuration template"""
        
        return {
            'model': {
                'name': f'{model_name}-tacrl',
                'base_model_path': 'Qwen/Qwen2.5-7B-Instruct',
                'model_type': 'qwen',
                'parameter_count': '7B',
                'context_length': 32768,
                'supports_function_calling': True
            },
            'training': {
                'algorithm': 'grpo',
                'batch_size': 4,
                'learning_rate': 1e-5,
                'max_episodes_per_task': 3,
                'reward_scale': 1.0,
                'current_phase': 'warmup',
                'tasks_per_phase': 15,
                'success_threshold': 0.6,
                'max_parallel_tasks': 2,
                'checkpoint_frequency': 50,
                'evaluation_frequency': 25,
                'output_dir': './outputs',
                'checkpoint_dir': './checkpoints',
                'log_dir': './logs'
            },
            'task_phases': {
                'warmup': [
                    'admin-make-spreadsheet',
                    'hr-check-attendance-one-day',
                    'ds-calculate-spreadsheet-stats'
                ],
                'intermediate': [
                    'admin-arrange-meeting-rooms',
                    'hr-check-attendance-multiple-days',
                    'finance-budget-variance'
                ],
                'advanced': [
                    'pm-create-plane-issue',
                    'admin-employee-info-reconciliation',
                    'ds-merge-multiple-sheets'
                ],
                'expert': []  # All remaining tasks
            },
            'openhands': {
                'max_iterations': 100,
                'timeout': 300,
                'enable_auto_lint': True,
                'use_host_network': True
            },
            'environment': {
                'server_hostname': 'localhost',
                'services': ['gitlab', 'plane', 'rocketchat', 'owncloud', 'api-server']
            },
            'monitoring': {
                'use_wandb': True,
                'project_name': 'tac-rl-training',
                'log_level': 'INFO',
                'save_trajectories': True,
                'realtime_monitoring': True
            }
        }
    
    def save_config(self, config: TrainingConfig, output_path: str):
        """Save configuration to YAML file"""
        
        # Convert TrainingConfig back to dictionary format
        config_dict = self._config_to_dict(config)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Configuration saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration to {output_path}: {e}")
            raise
    
    def _config_to_dict(self, config: TrainingConfig) -> Dict[str, Any]:
        """Convert TrainingConfig to dictionary format"""
        
        return {
            'model': {
                'name': config.model.name,
                'base_model_path': config.model.base_model_path,
                'model_type': config.model.model_type,
                'parameter_count': config.model.parameter_count,
                'context_length': config.model.context_length,
                'supports_function_calling': config.model.supports_function_calling
            },
            'training': {
                'algorithm': config.algorithm,
                'batch_size': config.batch_size,
                'learning_rate': config.learning_rate,
                'max_episodes_per_task': config.max_episodes_per_task,
                'reward_scale': config.reward_scale,
                'current_phase': config.current_phase.value,
                'tasks_per_phase': config.tasks_per_phase,
                'success_threshold': config.success_threshold,
                'max_parallel_tasks': config.max_parallel_tasks,
                'checkpoint_frequency': config.checkpoint_frequency,
                'evaluation_frequency': config.evaluation_frequency,
                'output_dir': config.output_dir,
                'checkpoint_dir': config.checkpoint_dir,
                'log_dir': config.log_dir
            },
            'openhands': getattr(config, 'openhands', {}),
            'environment': getattr(config, 'environment', {}),
            'monitoring': getattr(config, 'monitoring', {}),
            'task_phases': getattr(config, 'task_phases', {})
        }
    
    def update_config_from_env(self, config: TrainingConfig) -> TrainingConfig:
        """Update configuration with environment variables"""
        
        env_mappings = {
            'OPENAI_API_KEY': lambda c: setattr(c.model, 'api_key', os.environ.get('OPENAI_API_KEY')),
            'LLM_BASE_URL': lambda c: setattr(c.model, 'base_url', os.environ.get('LLM_BASE_URL')),
            'OPENPIPE_API_KEY': lambda c: setattr(c, 'openpipe_api_key', os.environ.get('OPENPIPE_API_KEY')),
            'WANDB_API_KEY': lambda c: c.monitoring.update({'wandb_api_key': os.environ.get('WANDB_API_KEY')}),
            'SERVER_HOSTNAME': lambda c: c.environment.update({'server_hostname': os.environ.get('SERVER_HOSTNAME', 'localhost')}),
        }
        
        for env_var, update_func in env_mappings.items():
            if os.environ.get(env_var):
                try:
                    update_func(config)
                    self.logger.debug(f"Updated config from {env_var}")
                except Exception as e:
                    self.logger.warning(f"Failed to update config from {env_var}: {e}")
        
        return config