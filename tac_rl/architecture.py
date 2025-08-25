"""
TAC-RL Architecture Design
==========================

This module defines the core architecture for training language models 
using reinforcement learning on TheAgentCompany benchmark.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import logging

class TaskDomain(Enum):
    """Professional task domains in TheAgentCompany"""
    ADMIN = "admin"
    HR = "hr" 
    FINANCE = "finance"
    DATA_SCIENCE = "ds"
    PROJECT_MANAGEMENT = "pm"
    SOFTWARE_ENGINEERING = "swe"
    MACHINE_LEARNING = "ml"
    BUSINESS = "bm"

class TrainingPhase(Enum):
    """Training phases for curriculum learning"""
    WARMUP = "warmup"          # Simple single-service tasks
    INTERMEDIATE = "intermediate"  # Multi-step tasks
    ADVANCED = "advanced"      # Complex multi-service tasks
    EXPERT = "expert"          # Full benchmark

@dataclass
class TaskConfig:
    """Configuration for individual tasks"""
    name: str
    domain: TaskDomain
    difficulty: int  # 1-5 scale
    services_required: List[str]  # ["gitlab", "plane", etc.]
    max_steps: int
    timeout_minutes: int
    checkpoint_count: int

@dataclass
class ModelConfig:
    """Model configuration for training"""
    name: str
    base_model_path: str
    model_type: str  # "qwen", "llama", "deepseek"
    parameter_count: str  # "7B", "14B", etc.
    context_length: int
    supports_function_calling: bool

@dataclass
class TrainingConfig:
    """Training configuration"""
    # Model settings
    model: ModelConfig
    
    # RL settings
    algorithm: str = "grpo"  # Group Relative Policy Optimization
    batch_size: int = 8
    learning_rate: float = 1e-5
    max_episodes_per_task: int = 3
    reward_scale: float = 1.0
    
    # Training phases
    current_phase: TrainingPhase = TrainingPhase.WARMUP
    tasks_per_phase: int = 20
    success_threshold: float = 0.7  # Move to next phase threshold
    
    # Infrastructure
    max_parallel_tasks: int = 4
    checkpoint_frequency: int = 100
    evaluation_frequency: int = 50
    
    # Paths
    output_dir: str = "./outputs"
    checkpoint_dir: str = "./checkpoints"
    log_dir: str = "./logs"

@dataclass 
class TrainingResult:
    """Result from a single training episode"""
    task_name: str
    success: bool
    reward: float
    steps_taken: int
    execution_time: float
    error_message: Optional[str] = None
    trajectory_path: Optional[str] = None
    checkpoints_passed: int = 0
    total_checkpoints: int = 0

class TACRLArchitecture:
    """Main architecture coordinator for TAC-RL system"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Component initialization will happen in setup
        self.task_sampler = None
        self.openhands_runner = None
        self.reward_computer = None
        self.art_trainer = None
        self.monitor = None
        
    def setup_components(self):
        """Initialize all system components with corrected integration"""
        from .components.task_sampler import TaskSampler
        from .components.local_art_trainer import LocalARTTrainer
        from .components.local_openhands_runner import LocalOpenHandsRunner
        from .components.reward_computer import RewardComputer
        from .components.monitor import TrainingMonitor
        
        self.logger.info("Setting up corrected TAC-RL components...")
        
        # 1. Initialize local ART trainer FIRST (this is the core model)
        self.art_trainer = LocalARTTrainer(self.config)
        
        # 2. Initialize OpenHands runner with reference to the SAME model
        self.openhands_runner = LocalOpenHandsRunner(
            self.config, 
            art_trainer=self.art_trainer  # Same model!
        )
        
        # 3. Initialize other components
        self.task_sampler = TaskSampler(self.config)
        self.reward_computer = RewardComputer(self.config)
        self.monitor = TrainingMonitor(self.config)
        
        self.logger.info("✅ Corrected components setup complete")
        self.logger.info(f"✅ Using local model: {self.config.model.base_model_path}")
        self.logger.info("✅ Same model used for execution AND training")
        
    async def train_iteration(self) -> List[TrainingResult]:
        """Execute one training iteration with corrected architecture"""
        
        self.logger.info("Starting corrected training iteration")
        
        # Sample tasks for current phase
        tasks = self.task_sampler.sample_batch(
            phase=self.config.current_phase,
            batch_size=self.config.batch_size
        )
        
        self.logger.info(f"Sampled {len(tasks)} tasks: {[t.name for t in tasks]}")
        
        # Execute tasks through OpenHands using the TRAINED model
        results = []
        for task in tasks:
            self.logger.info(f"Executing {task.name} with current trained model")
            result = await self.openhands_runner.execute_task(task)
            results.append(result)
            self.logger.info(f"Task {task.name}: success={result.success}")
        
        # Compute rewards based on outcomes
        rewards = []
        for result in results:
            reward = self.reward_computer.compute_reward(result)
            rewards.append(reward)
        
        # Update the model weights using ART with GRPO
        self.logger.info("Updating model weights with GRPO...")
        training_metrics = await self.art_trainer.train_step(results, rewards)
        self.logger.info(f"Training metrics: loss={training_metrics.get('loss', 'N/A')}")
        
        # The model is now better! Next iteration will use improved weights
        
        # Monitor progress
        if self.monitor:
            self.monitor.log_iteration(results, rewards)
        
        return results
        
    def should_advance_phase(self, recent_results: List[TrainingResult]) -> bool:
        """Determine if we should move to the next training phase"""
        if len(recent_results) < 20:  # Need sufficient data
            return False
            
        success_rate = sum(r.success for r in recent_results) / len(recent_results)
        return success_rate >= self.config.success_threshold
        
    def advance_phase(self):
        """Move to the next training phase"""
        current_phases = list(TrainingPhase)
        current_idx = current_phases.index(self.config.current_phase)
        
        if current_idx < len(current_phases) - 1:
            self.config.current_phase = current_phases[current_idx + 1]
            self.logger.info(f"Advanced to {self.config.current_phase.value} phase")
        else:
            self.logger.info("Already at final phase")