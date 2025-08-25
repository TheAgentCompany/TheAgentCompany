"""
Reward Computation System for TAC-RL
====================================

Computes sophisticated reward signals for reinforcement learning
based on TheAgentCompany evaluation results and intermediate progress.
"""

import logging
import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from ..architecture import TrainingResult, TrainingConfig, TaskDomain

class RewardType(Enum):
    """Types of rewards in the system"""
    TASK_COMPLETION = "task_completion"      # Binary success/failure
    CHECKPOINT_PROGRESS = "checkpoint_progress"  # Progress through checkpoints
    EFFICIENCY = "efficiency"                # Steps/time efficiency
    IMPROVEMENT = "improvement"              # Learning progress
    DOMAIN_BONUS = "domain_bonus"           # Domain-specific bonuses

@dataclass
class RewardComponents:
    """Breakdown of reward components"""
    task_completion: float = 0.0
    checkpoint_progress: float = 0.0
    efficiency_bonus: float = 0.0
    improvement_bonus: float = 0.0
    domain_bonus: float = 0.0
    penalty: float = 0.0
    total: float = 0.0

class RewardComputer:
    """Computes rewards for RL training"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Reward weights (configurable)
        self.weights = {
            RewardType.TASK_COMPLETION: 1.0,
            RewardType.CHECKPOINT_PROGRESS: 0.5,
            RewardType.EFFICIENCY: 0.2,
            RewardType.IMPROVEMENT: 0.3,
            RewardType.DOMAIN_BONUS: 0.1,
        }
        
        # Task performance history for improvement tracking
        self.task_history = {}
        
        # Domain-specific reward configurations
        self.domain_configs = self._setup_domain_configs()
        
    def _setup_domain_configs(self) -> Dict[TaskDomain, Dict[str, Any]]:
        """Setup domain-specific reward configurations"""
        return {
            TaskDomain.ADMIN: {
                'efficiency_weight': 1.2,  # Admin tasks value efficiency
                'accuracy_weight': 1.0,
                'bonus_keywords': ['spreadsheet', 'organize', 'schedule']
            },
            TaskDomain.HR: {
                'efficiency_weight': 0.8,
                'accuracy_weight': 1.3,    # HR tasks need high accuracy
                'bonus_keywords': ['policy', 'employee', 'compliance']
            },
            TaskDomain.FINANCE: {
                'efficiency_weight': 0.9,
                'accuracy_weight': 1.5,    # Finance requires highest accuracy
                'bonus_keywords': ['budget', 'reconciliation', 'tax']
            },
            TaskDomain.DATA_SCIENCE: {
                'efficiency_weight': 1.0,
                'accuracy_weight': 1.1,
                'bonus_keywords': ['analysis', 'model', 'visualization']
            },
            TaskDomain.PROJECT_MANAGEMENT: {
                'efficiency_weight': 1.1,
                'accuracy_weight': 1.0,
                'bonus_keywords': ['milestone', 'timeline', 'coordination']
            },
            TaskDomain.SOFTWARE_ENGINEERING: {
                'efficiency_weight': 1.0,
                'accuracy_weight': 1.2,
                'bonus_keywords': ['code', 'debug', 'test']
            },
            TaskDomain.MACHINE_LEARNING: {
                'efficiency_weight': 0.9,
                'accuracy_weight': 1.3,
                'bonus_keywords': ['train', 'evaluate', 'optimize']
            },
            TaskDomain.BUSINESS: {
                'efficiency_weight': 1.1,
                'accuracy_weight': 1.0,
                'bonus_keywords': ['strategy', 'market', 'analysis']
            }
        }
    
    def compute_reward(self, result: TrainingResult) -> float:
        """Compute total reward for a training result"""
        
        # Compute individual reward components
        components = self._compute_reward_components(result)
        
        # Apply reward scaling
        total_reward = components.total * self.config.reward_scale
        
        # Log detailed breakdown for debugging
        self.logger.debug(
            f"Reward for {result.task_name}: "
            f"completion={components.task_completion:.3f}, "
            f"progress={components.checkpoint_progress:.3f}, "
            f"efficiency={components.efficiency_bonus:.3f}, "
            f"improvement={components.improvement_bonus:.3f}, "
            f"domain={components.domain_bonus:.3f}, "
            f"penalty={components.penalty:.3f}, "
            f"total={total_reward:.3f}"
        )
        
        # Update task history for future improvement calculations
        self._update_task_history(result, components)
        
        return total_reward
    
    def _compute_reward_components(self, result: TrainingResult) -> RewardComponents:
        """Compute individual reward components"""
        
        components = RewardComponents()
        
        # 1. Task Completion Reward (binary success)
        components.task_completion = self._compute_completion_reward(result)
        
        # 2. Checkpoint Progress Reward (partial progress)
        components.checkpoint_progress = self._compute_progress_reward(result)
        
        # 3. Efficiency Bonus (steps and time)
        components.efficiency_bonus = self._compute_efficiency_reward(result)
        
        # 4. Improvement Bonus (learning progress)
        components.improvement_bonus = self._compute_improvement_reward(result)
        
        # 5. Domain-specific Bonus
        components.domain_bonus = self._compute_domain_bonus(result)
        
        # 6. Penalties (errors, timeouts, etc.)
        components.penalty = self._compute_penalties(result)
        
        # Combine components with weights
        total = 0.0
        for reward_type, weight in self.weights.items():
            if reward_type == RewardType.TASK_COMPLETION:
                total += components.task_completion * weight
            elif reward_type == RewardType.CHECKPOINT_PROGRESS:
                total += components.checkpoint_progress * weight
            elif reward_type == RewardType.EFFICIENCY:
                total += components.efficiency_bonus * weight
            elif reward_type == RewardType.IMPROVEMENT:
                total += components.improvement_bonus * weight
            elif reward_type == RewardType.DOMAIN_BONUS:
                total += components.domain_bonus * weight
        
        # Apply penalties
        total -= components.penalty
        
        # Ensure non-negative reward
        components.total = max(0.0, total)
        
        return components
    
    def _compute_completion_reward(self, result: TrainingResult) -> float:
        """Compute reward for task completion"""
        
        if result.success:
            # Base reward of 1.0 for successful completion
            base_reward = 1.0
            
            # Bonus for completing with fewer steps (efficiency)
            if result.steps_taken > 0:
                # Assume optimal is ~30 steps, give bonus for fewer
                optimal_steps = 30
                if result.steps_taken <= optimal_steps:
                    step_bonus = (optimal_steps - result.steps_taken) / optimal_steps * 0.2
                    base_reward += step_bonus
            
            return base_reward
        else:
            # No reward for failure, but checkpoint progress may still give some reward
            return 0.0
    
    def _compute_progress_reward(self, result: TrainingResult) -> float:
        """Compute reward for checkpoint progress"""
        
        if result.total_checkpoints == 0:
            return 0.0
        
        # Progress reward based on checkpoints passed
        progress_ratio = result.checkpoints_passed / result.total_checkpoints
        
        # Use square root to give diminishing returns for later checkpoints
        # This encourages getting started but doesn't over-reward partial completion
        progress_reward = math.sqrt(progress_ratio) * 0.5
        
        # Bonus for high progress even without full completion
        if progress_ratio >= 0.8 and not result.success:
            progress_reward += 0.2  # "Almost there" bonus
        
        return progress_reward
    
    def _compute_efficiency_reward(self, result: TrainingResult) -> float:
        """Compute reward for efficiency (steps and time)"""
        
        if not result.success:
            return 0.0  # Only reward efficiency on successful tasks
        
        efficiency_reward = 0.0
        
        # Step efficiency
        if result.steps_taken > 0:
            # Reward fewer steps (assume 50 is reasonable, 30 is good, 20 is excellent)
            if result.steps_taken <= 20:
                efficiency_reward += 0.3  # Excellent
            elif result.steps_taken <= 30:
                efficiency_reward += 0.2  # Good
            elif result.steps_taken <= 50:
                efficiency_reward += 0.1  # Reasonable
            # No bonus for >50 steps
        
        # Time efficiency  
        if result.execution_time > 0:
            # Reward faster completion (assume 10 min reasonable, 5 min good, 3 min excellent)
            time_minutes = result.execution_time / 60
            if time_minutes <= 3:
                efficiency_reward += 0.2  # Excellent
            elif time_minutes <= 5:
                efficiency_reward += 0.15  # Good
            elif time_minutes <= 10:
                efficiency_reward += 0.1  # Reasonable
            # No bonus for >10 minutes
        
        return efficiency_reward
    
    def _compute_improvement_reward(self, result: TrainingResult) -> float:
        """Compute reward for learning improvement over time"""
        
        task_name = result.task_name
        
        # Need history to compute improvement
        if task_name not in self.task_history or len(self.task_history[task_name]) < 2:
            return 0.0
        
        history = self.task_history[task_name]
        recent_results = history[-5:]  # Last 5 attempts
        
        # Compare current performance to recent average
        recent_success_rate = sum(r['success'] for r in recent_results) / len(recent_results)
        recent_avg_steps = sum(r['steps'] for r in recent_results) / len(recent_results)
        
        improvement_reward = 0.0
        
        # Reward for improvement in success rate
        if result.success and recent_success_rate < 0.8:
            improvement_reward += 0.2
        
        # Reward for improvement in efficiency
        if result.success and result.steps_taken < recent_avg_steps * 0.8:
            improvement_reward += 0.1
        
        return improvement_reward
    
    def _compute_domain_bonus(self, result: TrainingResult) -> float:
        """Compute domain-specific bonus rewards"""
        
        # This would need task domain information
        # For now, return a simple bonus for successful completion
        if result.success:
            return 0.1
        return 0.0
    
    def _compute_penalties(self, result: TrainingResult) -> float:
        """Compute penalty for errors, inefficiencies, etc."""
        
        penalty = 0.0
        
        # Penalty for errors
        if result.error_message:
            penalty += 0.2
        
        # Penalty for taking too many steps
        if result.steps_taken > 100:
            penalty += 0.1
        
        # Penalty for taking too long (relative to task timeout)
        # This would need task timeout info from config
        if result.execution_time > 1800:  # 30 minutes
            penalty += 0.15
        
        return penalty
    
    def _update_task_history(self, result: TrainingResult, components: RewardComponents):
        """Update task performance history for improvement tracking"""
        
        task_name = result.task_name
        
        if task_name not in self.task_history:
            self.task_history[task_name] = []
        
        # Store relevant metrics
        self.task_history[task_name].append({
            'success': result.success,
            'steps': result.steps_taken,
            'time': result.execution_time,
            'reward': components.total,
            'checkpoints_passed': result.checkpoints_passed,
        })
        
        # Keep only last 20 results to manage memory
        self.task_history[task_name] = self.task_history[task_name][-20:]
    
    def get_reward_statistics(self) -> Dict[str, Any]:
        """Get statistics about reward distribution"""
        
        if not self.task_history:
            return {}
        
        all_rewards = []
        success_rewards = []
        failure_rewards = []
        
        for task_results in self.task_history.values():
            for result in task_results:
                all_rewards.append(result['reward'])
                if result['success']:
                    success_rewards.append(result['reward'])
                else:
                    failure_rewards.append(result['reward'])
        
        def safe_mean(lst):
            return sum(lst) / len(lst) if lst else 0.0
        
        return {
            'total_episodes': len(all_rewards),
            'mean_reward': safe_mean(all_rewards),
            'mean_success_reward': safe_mean(success_rewards),
            'mean_failure_reward': safe_mean(failure_rewards),
            'success_rate': len(success_rewards) / len(all_rewards) if all_rewards else 0.0,
            'reward_range': {
                'min': min(all_rewards) if all_rewards else 0.0,
                'max': max(all_rewards) if all_rewards else 0.0,
            }
        }
    
    def adjust_reward_weights(self, adjustments: Dict[RewardType, float]):
        """Adjust reward component weights during training"""
        
        for reward_type, adjustment in adjustments.items():
            if reward_type in self.weights:
                self.weights[reward_type] = max(0.0, self.weights[reward_type] + adjustment)
                self.logger.info(f"Adjusted {reward_type.value} weight to {self.weights[reward_type]:.3f}")
    
    def reset_history(self):
        """Reset task history (useful for new training runs)"""
        self.task_history.clear()
        self.logger.info("Reset reward computation history")