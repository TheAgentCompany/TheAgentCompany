"""
Local OpenPipe ART Training Integration for TAC-RL
=================================================

Real implementation using OpenPipe ART for local model training
with LoRA fine-tuning and GRPO optimization.
"""

import logging
import json
import os
import tempfile
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# OpenPipe ART imports - the real deal
try:
    import art
    from art import LocalBackend, TrainableModel, TrainConfig, Trajectory, TrajectoryGroup
    from art.rewards import ruler_score_group
    HAS_ART = True
except ImportError:
    HAS_ART = False
    logging.warning("OpenPipe ART not installed. Install with: pip install openpipe-art")

from ..architecture import TrainingResult, TrainingConfig

class LocalARTTrainer:
    """Real OpenPipe ART integration for local model training"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        if not HAS_ART:
            raise ImportError("OpenPipe ART required. Install with: pip install openpipe-art")
        
        # Initialize local ART backend
        self.backend = None
        self.model = None
        self.training_step = 0
        
        # Setup model and training environment
        self._setup_art_model()
        
    def _setup_art_model(self):
        """Setup local ART model for training"""
        
        try:
            # Initialize local backend (runs on your GPU)
            self.backend = LocalBackend()
            
            # Configure LoRA for efficient fine-tuning
            peft_config = {
                "r": 8,              # LoRA rank
                "lora_alpha": 16,    # LoRA scaling
                "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj", 
                                 "gate_proj", "up_proj", "down_proj"],
                "lora_dropout": 0.1,
                "bias": "none",
                "task_type": "CAUSAL_LM"
            }
            
            # Create trainable model
            self.model = TrainableModel(
                backend=self.backend,
                base_model=self.config.model.base_model_path,  # e.g., "Qwen/Qwen2.5-7B-Instruct"
                peft_config=peft_config
            )
            
            self.logger.info(f"ART model initialized: {self.config.model.base_model_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ART model: {e}")
            raise
    
    async def train_step(self, results: List[TrainingResult], rewards: List[float]):
        """Execute one training step with collected results"""
        
        self.training_step += 1
        
        try:
            self.logger.info(f"Starting ART training step {self.training_step}")
            
            # Convert TAC-RL results to ART trajectories
            trajectory_groups = await self._prepare_trajectory_groups(results, rewards)
            
            if not trajectory_groups:
                self.logger.warning("No valid trajectory groups for training")
                return {"loss": float('inf'), "examples_processed": 0}
            
            # Perform actual model training with GRPO
            training_metrics = await self._execute_grpo_training(trajectory_groups)
            
            self.logger.info(f"ART training step {self.training_step} completed")
            return training_metrics
            
        except Exception as e:
            self.logger.error(f"ART training step {self.training_step} failed: {e}", exc_info=True)
            return {"loss": float('inf'), "examples_processed": 0, "error": str(e)}
    
    async def _prepare_trajectory_groups(
        self, 
        results: List[TrainingResult], 
        rewards: List[float]
    ) -> List[TrajectoryGroup]:
        """Convert TAC-RL results to ART trajectory groups"""
        
        trajectory_groups = []
        
        for result, reward in zip(results, rewards):
            try:
                # Load trajectory from OpenHands execution
                trajectory_data = self._load_trajectory_data(result.trajectory_path)
                if not trajectory_data:
                    continue
                
                # Convert to ART trajectory format
                art_trajectory = await self._convert_to_art_trajectory(
                    trajectory_data, result, reward
                )
                
                if art_trajectory:
                    # Create trajectory group (can have multiple trajectories per task)
                    group = TrajectoryGroup(trajectories=[art_trajectory])
                    trajectory_groups.append(group)
                    
            except Exception as e:
                self.logger.warning(f"Failed to process trajectory for {result.task_name}: {e}")
                
        self.logger.info(f"Prepared {len(trajectory_groups)} trajectory groups")
        return trajectory_groups
    
    def _load_trajectory_data(self, trajectory_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Load trajectory data from OpenHands execution"""
        
        if not trajectory_path or not os.path.exists(trajectory_path):
            return None
            
        try:
            with open(trajectory_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load trajectory from {trajectory_path}: {e}")
            return None
    
    async def _convert_to_art_trajectory(
        self, 
        trajectory_data: Dict[str, Any], 
        result: TrainingResult, 
        reward: float
    ) -> Optional[Trajectory]:
        """Convert OpenHands trajectory to ART format"""
        
        try:
            # Extract messages from OpenHands history
            messages = []
            
            # Add initial task instruction
            task_instruction = f"Complete the task: {result.task_name}\n\nTask details are in /instruction/task.md"
            messages.append({"role": "user", "content": task_instruction})
            
            # Process OpenHands history
            if 'history' in trajectory_data:
                for event in trajectory_data['history']:
                    if isinstance(event, dict):
                        # Convert different event types to messages
                        if event.get('action') == 'message':
                            role = 'user' if event.get('source') == 'user' else 'assistant'
                            content = event.get('args', {}).get('content', '')
                            if content.strip():
                                messages.append({"role": role, "content": content})
                        
                        elif event.get('action') == 'run':
                            # Command execution
                            command = event.get('args', {}).get('command', '')
                            if command.strip():
                                messages.append({
                                    "role": "assistant",
                                    "content": f"I'll run this command: {command}"
                                })
                        
                        elif 'observation' in event:
                            # Command output (limit length)
                            output = event.get('content', '')[:500]  # Truncate long outputs
                            if output.strip():
                                messages.append({
                                    "role": "system", 
                                    "content": f"Output: {output}"
                                })
            
            # Create ART trajectory
            trajectory = Trajectory(
                messages=messages,
                reward=reward,
                metadata={
                    "task_name": result.task_name,
                    "success": result.success,
                    "steps_taken": result.steps_taken,
                    "execution_time": result.execution_time,
                    "checkpoints_passed": result.checkpoints_passed
                }
            )
            
            return trajectory
            
        except Exception as e:
            self.logger.error(f"Failed to convert trajectory: {e}")
            return None
    
    async def _execute_grpo_training(self, trajectory_groups: List[TrajectoryGroup]) -> Dict[str, Any]:
        """Execute GRPO training with ART"""
        
        try:
            # Filter valid trajectory groups
            valid_groups = [g for g in trajectory_groups if g.trajectories]
            
            if not valid_groups:
                return {"loss": float('inf'), "examples_processed": 0}
            
            # Use RULER for automatic reward scoring if no manual rewards
            scored_groups = []
            for group in valid_groups:
                try:
                    # Use OpenPipe's RULER for trajectory ranking
                    scored_group = await ruler_score_group(
                        group, 
                        "openai/gpt-4o-mini",  # Judge model
                        task_description="Complete professional tasks accurately and efficiently"
                    )
                    scored_groups.append(scored_group)
                except Exception as e:
                    self.logger.debug(f"RULER scoring failed, using original rewards: {e}")
                    scored_groups.append(group)
            
            # Execute actual model training
            train_config = TrainConfig(
                learning_rate=self.config.learning_rate,
                epochs=1,  # One epoch per training step
                batch_size=min(len(scored_groups), self.config.batch_size)
            )
            
            self.logger.info(f"Training model on {len(scored_groups)} trajectory groups")
            
            # This is the actual weight update!
            training_result = await self.model.train(
                trajectory_groups=scored_groups,
                config=train_config
            )
            
            # Extract training metrics
            metrics = {
                "loss": training_result.get("loss", 0.0),
                "learning_rate": self.config.learning_rate,
                "examples_processed": len(scored_groups),
                "training_step": self.training_step
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"GRPO training failed: {e}", exc_info=True)
            return {"loss": float('inf'), "examples_processed": 0, "error": str(e)}
    
    async def generate_completion(self, messages: List[Dict[str, str]]) -> str:
        """Generate completion using the trained model"""
        
        try:
            # Use the trained model for inference
            response = await self.model.generate(messages=messages)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return ""
    
    def save_checkpoint(self, checkpoint_path: str):
        """Save model checkpoint"""
        
        try:
            checkpoint_data = {
                'training_step': self.training_step,
                'model_config': {
                    'base_model': self.config.model.base_model_path,
                    'parameter_count': self.config.model.parameter_count
                },
                'training_config': {
                    'learning_rate': self.config.learning_rate,
                    'batch_size': self.config.batch_size
                },
                'timestamp': datetime.now().isoformat()
            }
            
            # Save metadata
            Path(checkpoint_path).parent.mkdir(parents=True, exist_ok=True)
            with open(f"{checkpoint_path}.json", 'w') as f:
                json.dump(checkpoint_data, f, indent=2)
            
            # Save actual model weights (LoRA adapters)
            if self.model:
                self.model.save_pretrained(checkpoint_path)
            
            self.logger.info(f"Checkpoint saved: {checkpoint_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save checkpoint: {e}")
    
    def load_checkpoint(self, checkpoint_path: str) -> bool:
        """Load model from checkpoint"""
        
        try:
            # Load metadata
            with open(f"{checkpoint_path}.json", 'r') as f:
                checkpoint_data = json.load(f)
            
            self.training_step = checkpoint_data.get('training_step', 0)
            
            # Load model weights
            if self.model and os.path.exists(checkpoint_path):
                self.model.load_adapter(checkpoint_path)
            
            self.logger.info(f"Checkpoint loaded: {checkpoint_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load checkpoint: {e}")
            return False
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status"""
        
        return {
            'training_step': self.training_step,
            'model_path': self.config.model.base_model_path,
            'backend_type': 'LocalBackend',
            'has_model': self.model is not None,
            'training_config': {
                'learning_rate': self.config.learning_rate,
                'batch_size': self.config.batch_size
            }
        }
    
    def cleanup(self):
        """Clean up resources"""
        
        self.logger.info("Cleaning up LocalART trainer")
        
        if self.model:
            try:
                # Clean up model resources
                del self.model
            except:
                pass
        
        if self.backend:
            try:
                # Clean up backend resources
                del self.backend
            except:
                pass