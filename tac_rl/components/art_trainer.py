"""
OpenPipe ART Training Integration for TAC-RL
===========================================

Integrates OpenPipe's Agent Reinforcement Trainer (ART) for 
GRPO-based training on TheAgentCompany tasks.
"""

import logging
import json
import os
import tempfile
from typing import List, Dict, Any, Optional
from pathlib import Path
import asyncio
from datetime import datetime

# OpenPipe ART imports (these would be actual imports in production)
try:
    import openpipe
    from openpipe import OpenPipe
    HAS_OPENPIPE = True
except ImportError:
    # Fallback for development - create mock classes
    HAS_OPENPIPE = False
    class OpenPipe:
        def __init__(self, *args, **kwargs):
            pass
        def log(self, *args, **kwargs):
            pass
    
from ..architecture import TrainingResult, TrainingConfig

class ARTTrainer:
    """OpenPipe ART integration for model training"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenPipe client
        self._init_openpipe_client()
        
        # Training state
        self.training_step = 0
        self.episode_trajectories = []
        self.episode_rewards = []
        
        # Model checkpoint management
        self.best_model_score = 0.0
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
    def _init_openpipe_client(self):
        """Initialize OpenPipe ART client"""
        
        if not HAS_OPENPIPE:
            self.logger.warning("OpenPipe not available, using mock client")
            self.openpipe_client = OpenPipe()
            return
        
        # Get API key from environment
        api_key = os.environ.get('OPENPIPE_API_KEY')
        if not api_key:
            self.logger.warning("OPENPIPE_API_KEY not set, some features may not work")
        
        try:
            # Initialize OpenPipe client for GRPO training
            self.openpipe_client = OpenPipe(
                api_key=api_key,
                base_url=os.environ.get('OPENPIPE_BASE_URL', 'https://api.openpipe.ai/api/v1')
            )
            
            self.logger.info("OpenPipe ART client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenPipe client: {e}")
            self.openpipe_client = OpenPipe()  # Use mock
    
    def train_step(self, results: List[TrainingResult], rewards: List[float]):
        """Execute one training step with collected results"""
        
        self.training_step += 1
        
        try:
            self.logger.info(f"Starting training step {self.training_step}")
            
            # Convert results to training format
            training_data = self._prepare_training_data(results, rewards)
            
            # Execute GRPO training step
            training_metrics = self._execute_grpo_step(training_data)
            
            # Update model checkpoints if improved
            self._maybe_save_checkpoint(training_metrics)
            
            # Log training progress
            self._log_training_metrics(training_metrics, rewards)
            
            self.logger.info(f"Training step {self.training_step} completed")
            
        except Exception as e:
            self.logger.error(f"Training step {self.training_step} failed: {e}", exc_info=True)
            raise
    
    def _prepare_training_data(
        self, 
        results: List[TrainingResult], 
        rewards: List[float]
    ) -> List[Dict[str, Any]]:
        """Convert TAC-RL results to OpenPipe ART training format"""
        
        training_data = []
        
        for result, reward in zip(results, rewards):
            
            # Load trajectory if available
            trajectory = self._load_trajectory(result.trajectory_path)
            
            if not trajectory:
                self.logger.warning(f"No trajectory available for {result.task_name}")
                continue
            
            # Convert to OpenPipe format
            training_example = {
                'task_id': result.task_name,
                'messages': self._extract_messages_from_trajectory(trajectory),
                'reward': reward,
                'success': result.success,
                'metadata': {
                    'steps_taken': result.steps_taken,
                    'execution_time': result.execution_time,
                    'checkpoints_passed': result.checkpoints_passed,
                    'total_checkpoints': result.total_checkpoints,
                    'domain': self._infer_domain_from_task_name(result.task_name),
                }
            }
            
            training_data.append(training_example)
        
        self.logger.info(f"Prepared {len(training_data)} training examples")
        return training_data
    
    def _load_trajectory(self, trajectory_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Load trajectory data from file"""
        
        if not trajectory_path or not os.path.exists(trajectory_path):
            return None
        
        try:
            with open(trajectory_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load trajectory from {trajectory_path}: {e}")
            return None
    
    def _extract_messages_from_trajectory(self, trajectory: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract messages from OpenHands trajectory for training"""
        
        messages = []
        
        # Extract from OpenHands trajectory format
        if 'history' in trajectory:
            for event in trajectory['history']:
                if isinstance(event, dict):
                    # Message actions
                    if event.get('action') == 'message':
                        role = 'user' if event.get('source') == 'user' else 'assistant'
                        content = event.get('args', {}).get('content', '')
                        if content:
                            messages.append({'role': role, 'content': content})
                    
                    # Command actions
                    elif event.get('action') == 'run':
                        command = event.get('args', {}).get('command', '')
                        if command:
                            messages.append({
                                'role': 'assistant',
                                'content': f'<execute_bash>{command}</execute_bash>'
                            })
                    
                    # Observations
                    elif event.get('observation'):
                        obs_content = event.get('content', '')
                        if obs_content and len(obs_content) < 1000:  # Limit observation length
                            messages.append({
                                'role': 'system',
                                'content': f'Command output: {obs_content}'
                            })
        
        return messages
    
    def _execute_grpo_step(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute GRPO training step using OpenPipe ART"""
        
        if not HAS_OPENPIPE:
            # Mock training metrics for development
            return {
                'loss': 0.5 - (self.training_step * 0.01),  # Decreasing loss
                'policy_loss': 0.3,
                'value_loss': 0.2,
                'learning_rate': self.config.learning_rate,
                'grad_norm': 1.5,
                'examples_processed': len(training_data)
            }
        
        try:
            # Use OpenPipe ART for GRPO training
            training_job = self.openpipe_client.train(
                model=self.config.model.base_model_path,
                training_data=training_data,
                config={
                    'algorithm': 'grpo',
                    'batch_size': self.config.batch_size,
                    'learning_rate': self.config.learning_rate,
                    'max_steps': 1,  # Single step
                    'reward_scale': self.config.reward_scale,
                }
            )
            
            # Wait for completion (for single step this should be quick)
            result = training_job.wait()
            
            return {
                'loss': result.get('loss', 0.0),
                'policy_loss': result.get('policy_loss', 0.0),
                'value_loss': result.get('value_loss', 0.0),
                'learning_rate': self.config.learning_rate,
                'grad_norm': result.get('grad_norm', 0.0),
                'examples_processed': len(training_data),
                'job_id': training_job.id
            }
            
        except Exception as e:
            self.logger.error(f"GRPO training step failed: {e}")
            # Return fallback metrics
            return {
                'loss': float('inf'),
                'policy_loss': float('inf'), 
                'value_loss': float('inf'),
                'learning_rate': self.config.learning_rate,
                'grad_norm': 0.0,
                'examples_processed': len(training_data),
                'error': str(e)
            }
    
    def _maybe_save_checkpoint(self, training_metrics: Dict[str, Any]):
        """Save model checkpoint if performance improved"""
        
        # Use negative loss as score (lower loss = higher score)
        current_score = -training_metrics.get('loss', float('inf'))
        
        if current_score > self.best_model_score:
            self.best_model_score = current_score
            
            checkpoint_path = self.checkpoint_dir / f'checkpoint_step_{self.training_step}.pt'
            
            try:
                # Save checkpoint (this would be actual model saving in production)
                checkpoint_data = {
                    'step': self.training_step,
                    'score': current_score,
                    'metrics': training_metrics,
                    'config': self.config.__dict__,
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(checkpoint_path, 'w') as f:
                    json.dump(checkpoint_data, f, indent=2)
                
                self.logger.info(f"Saved checkpoint at step {self.training_step} with score {current_score:.4f}")
                
                # Also save as "best" checkpoint
                best_path = self.checkpoint_dir / 'best_checkpoint.pt'
                with open(best_path, 'w') as f:
                    json.dump(checkpoint_data, f, indent=2)
                
            except Exception as e:
                self.logger.error(f"Failed to save checkpoint: {e}")
    
    def _log_training_metrics(self, training_metrics: Dict[str, Any], rewards: List[float]):
        """Log training metrics"""
        
        # Calculate reward statistics
        mean_reward = sum(rewards) / len(rewards) if rewards else 0.0
        max_reward = max(rewards) if rewards else 0.0
        min_reward = min(rewards) if rewards else 0.0
        
        # Log to console
        self.logger.info(
            f"Step {self.training_step}: "
            f"loss={training_metrics.get('loss', 0.0):.4f}, "
            f"mean_reward={mean_reward:.4f}, "
            f"max_reward={max_reward:.4f}, "
            f"examples={training_metrics.get('examples_processed', 0)}"
        )
        
        # Log to OpenPipe (if available)
        if HAS_OPENPIPE:
            try:
                self.openpipe_client.log({
                    'step': self.training_step,
                    'loss': training_metrics.get('loss', 0.0),
                    'policy_loss': training_metrics.get('policy_loss', 0.0),
                    'value_loss': training_metrics.get('value_loss', 0.0),
                    'mean_reward': mean_reward,
                    'max_reward': max_reward,
                    'min_reward': min_reward,
                    'learning_rate': self.config.learning_rate,
                    'examples_processed': training_metrics.get('examples_processed', 0)
                })
            except Exception as e:
                self.logger.debug(f"Failed to log to OpenPipe: {e}")
    
    def _infer_domain_from_task_name(self, task_name: str) -> str:
        """Infer task domain from name"""
        domain_prefixes = {
            'admin-': 'administration',
            'hr-': 'human_resources',
            'finance-': 'finance',
            'ds-': 'data_science',
            'pm-': 'project_management',
            'swe-': 'software_engineering',
            'ml-': 'machine_learning',
            'bm-': 'business'
        }
        
        for prefix, domain in domain_prefixes.items():
            if task_name.startswith(prefix):
                return domain
        
        return 'unknown'
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status"""
        
        return {
            'training_step': self.training_step,
            'best_model_score': self.best_model_score,
            'model_config': {
                'name': self.config.model.name,
                'base_model': self.config.model.base_model_path,
                'parameter_count': self.config.model.parameter_count
            },
            'training_config': {
                'algorithm': self.config.algorithm,
                'batch_size': self.config.batch_size,
                'learning_rate': self.config.learning_rate,
                'reward_scale': self.config.reward_scale
            },
            'checkpoint_dir': str(self.checkpoint_dir)
        }
    
    def load_checkpoint(self, checkpoint_path: str) -> bool:
        """Load model from checkpoint"""
        
        try:
            if not os.path.exists(checkpoint_path):
                self.logger.error(f"Checkpoint not found: {checkpoint_path}")
                return False
            
            with open(checkpoint_path, 'r') as f:
                checkpoint_data = json.load(f)
            
            self.training_step = checkpoint_data.get('step', 0)
            self.best_model_score = checkpoint_data.get('score', 0.0)
            
            self.logger.info(
                f"Loaded checkpoint from step {self.training_step} "
                f"with score {self.best_model_score:.4f}"
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load checkpoint: {e}")
            return False
    
    def cleanup(self):
        """Clean up training resources"""
        self.logger.info("Cleaning up ART trainer resources")
        
        # Clear trajectory cache
        self.episode_trajectories.clear()
        self.episode_rewards.clear()
        
        # Any other cleanup needed for OpenPipe
        if hasattr(self.openpipe_client, 'close'):
            try:
                self.openpipe_client.close()
            except:
                pass