"""
Task Sampling System for TAC-RL
===============================

Handles intelligent sampling of tasks from TheAgentCompany benchmark
for curriculum-based reinforcement learning training.
"""

import os
import random
import yaml
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import logging

from ..architecture import TaskDomain, TrainingPhase, TaskConfig

@dataclass
class TaskMetadata:
    """Metadata for a TheAgentCompany task"""
    name: str
    path: str
    domain: TaskDomain
    services_required: List[str]
    difficulty_estimate: int  # 1-5 scale
    avg_completion_time: float  # minutes
    success_rate_baseline: float  # baseline success rate
    has_dependencies: bool
    checkpoint_count: int

class TaskSampler:
    """Intelligent task sampling for curriculum learning"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load task metadata
        self.task_metadata = self._load_task_metadata()
        self.task_history = {}  # Track performance per task
        
        # Phase-specific task pools
        self.phase_tasks = self._organize_tasks_by_phase()
        
    def _load_task_metadata(self) -> Dict[str, TaskMetadata]:
        """Load metadata for all available tasks"""
        self.logger.info("Loading task metadata from TheAgentCompany...")
        
        metadata = {}
        tasks_dir = Path("workspaces/tasks")
        
        if not tasks_dir.exists():
            self.logger.error(f"Tasks directory not found: {tasks_dir}")
            return metadata
            
        for task_dir in tasks_dir.iterdir():
            if not task_dir.is_dir() or task_dir.name.startswith('.'):
                continue
                
            task_name = task_dir.name
            try:
                task_meta = self._parse_task_metadata(task_dir, task_name)
                if task_meta:
                    metadata[task_name] = task_meta
            except Exception as e:
                self.logger.warning(f"Failed to parse metadata for {task_name}: {e}")
                
        self.logger.info(f"Loaded metadata for {len(metadata)} tasks")
        return metadata
        
    def _parse_task_metadata(self, task_dir: Path, task_name: str) -> Optional[TaskMetadata]:
        """Parse metadata for a single task"""
        
        # Determine domain from task name prefix
        domain = self._infer_domain(task_name)
        
        # Load dependencies
        deps_file = task_dir / "dependencies.yml"
        services_required = []
        if deps_file.exists():
            try:
                with open(deps_file, 'r') as f:
                    deps = yaml.safe_load(f) or []
                    services_required = deps if isinstance(deps, list) else []
            except Exception as e:
                self.logger.debug(f"Could not load dependencies for {task_name}: {e}")
        
        # Count checkpoints
        checkpoints_file = task_dir / "checkpoints.md"
        checkpoint_count = self._count_checkpoints(checkpoints_file)
        
        # Estimate difficulty based on various factors
        difficulty = self._estimate_difficulty(
            task_name, services_required, checkpoint_count
        )
        
        return TaskMetadata(
            name=task_name,
            path=str(task_dir),
            domain=domain,
            services_required=services_required,
            difficulty_estimate=difficulty,
            avg_completion_time=10.0 + difficulty * 5.0,  # Rough estimate
            success_rate_baseline=max(0.1, 0.8 - difficulty * 0.15),
            has_dependencies=len(services_required) > 0,
            checkpoint_count=checkpoint_count
        )
    
    def _infer_domain(self, task_name: str) -> TaskDomain:
        """Infer task domain from name prefix"""
        domain_map = {
            'admin-': TaskDomain.ADMIN,
            'hr-': TaskDomain.HR,
            'finance-': TaskDomain.FINANCE,
            'ds-': TaskDomain.DATA_SCIENCE,
            'pm-': TaskDomain.PROJECT_MANAGEMENT,
            'swe-': TaskDomain.SOFTWARE_ENGINEERING,
            'ml-': TaskDomain.MACHINE_LEARNING,
            'bm-': TaskDomain.BUSINESS,
        }
        
        for prefix, domain in domain_map.items():
            if task_name.startswith(prefix):
                return domain
                
        # Default fallback
        return TaskDomain.ADMIN
    
    def _count_checkpoints(self, checkpoints_file: Path) -> int:
        """Count number of checkpoints in a task"""
        if not checkpoints_file.exists():
            return 1  # Default minimum
            
        try:
            with open(checkpoints_file, 'r') as f:
                content = f.read()
                # Count markdown headers or checkpoint patterns
                checkpoint_patterns = ['##', '- [ ]', 'checkpoint', 'step']
                count = sum(content.lower().count(pattern) for pattern in checkpoint_patterns)
                return max(1, min(count, 10))  # Clamp between 1-10
        except Exception:
            return 1
    
    def _estimate_difficulty(self, task_name: str, services: List[str], checkpoints: int) -> int:
        """Estimate task difficulty on 1-5 scale"""
        difficulty = 1
        
        # Base difficulty from services required
        if len(services) == 0:
            difficulty += 0
        elif len(services) == 1:
            difficulty += 1
        elif len(services) <= 2:
            difficulty += 2
        else:
            difficulty += 3
            
        # Adjust for checkpoints
        if checkpoints > 5:
            difficulty += 1
        elif checkpoints > 8:
            difficulty += 2
            
        # Adjust for task type keywords
        complex_keywords = [
            'multiple', 'complex', 'spreadsheet', 'database', 
            'analysis', 'reconciliation', 'integration'
        ]
        
        for keyword in complex_keywords:
            if keyword in task_name.lower():
                difficulty += 1
                break
                
        return max(1, min(difficulty, 5))  # Clamp 1-5
    
    def _organize_tasks_by_phase(self) -> Dict[TrainingPhase, List[str]]:
        """Organize tasks into training phases based on difficulty"""
        phase_tasks = {phase: [] for phase in TrainingPhase}
        
        for task_name, metadata in self.task_metadata.items():
            # Assign to phase based on difficulty and dependencies
            if metadata.difficulty_estimate <= 2 and len(metadata.services_required) <= 1:
                phase_tasks[TrainingPhase.WARMUP].append(task_name)
            elif metadata.difficulty_estimate <= 3 and len(metadata.services_required) <= 2:
                phase_tasks[TrainingPhase.INTERMEDIATE].append(task_name)
            elif metadata.difficulty_estimate <= 4:
                phase_tasks[TrainingPhase.ADVANCED].append(task_name)
            else:
                phase_tasks[TrainingPhase.EXPERT].append(task_name)
        
        # Log distribution
        for phase, tasks in phase_tasks.items():
            self.logger.info(f"{phase.value}: {len(tasks)} tasks")
            
        return phase_tasks
    
    def sample_batch(self, phase: TrainingPhase, batch_size: int) -> List[TaskConfig]:
        """Sample a batch of tasks for the given training phase"""
        
        available_tasks = self.phase_tasks.get(phase, [])
        if not available_tasks:
            self.logger.warning(f"No tasks available for phase {phase.value}")
            return []
        
        # Intelligent sampling based on performance history
        sampled_names = self._intelligent_sample(available_tasks, batch_size)
        
        # Convert to TaskConfig objects
        batch = []
        for task_name in sampled_names:
            metadata = self.task_metadata[task_name]
            task_config = TaskConfig(
                name=task_name,
                domain=metadata.domain,
                difficulty=metadata.difficulty_estimate,
                services_required=metadata.services_required,
                max_steps=100,  # Default from OpenHands
                timeout_minutes=int(metadata.avg_completion_time * 2),  # 2x estimate
                checkpoint_count=metadata.checkpoint_count
            )
            batch.append(task_config)
            
        self.logger.info(f"Sampled batch of {len(batch)} tasks for {phase.value} phase")
        return batch
    
    def _intelligent_sample(self, available_tasks: List[str], batch_size: int) -> List[str]:
        """Intelligently sample tasks based on performance history"""
        
        # If we have fewer tasks than batch size, return all
        if len(available_tasks) <= batch_size:
            return available_tasks.copy()
        
        # Calculate sampling weights based on performance
        task_weights = {}
        
        for task_name in available_tasks:
            weight = 1.0  # Base weight
            
            # If we have history for this task
            if task_name in self.task_history:
                history = self.task_history[task_name]
                recent_success_rate = self._calculate_recent_success_rate(history)
                
                # Sample more frequently if struggling (lower success rate)
                if recent_success_rate < 0.3:
                    weight = 2.0  # Higher chance to retry
                elif recent_success_rate < 0.6:
                    weight = 1.5
                elif recent_success_rate > 0.8:
                    weight = 0.5  # Less chance if mastered
                    
            task_weights[task_name] = weight
        
        # Weighted random sampling
        tasks = list(task_weights.keys())
        weights = list(task_weights.values())
        
        sampled = random.choices(tasks, weights=weights, k=batch_size)
        
        # Ensure no duplicates in batch
        sampled = list(dict.fromkeys(sampled))  # Preserves order, removes duplicates
        
        # If we need more due to duplicates, randomly fill
        while len(sampled) < batch_size and len(sampled) < len(available_tasks):
            remaining = [t for t in available_tasks if t not in sampled]
            if remaining:
                sampled.append(random.choice(remaining))
        
        return sampled
    
    def _calculate_recent_success_rate(self, history: List[Dict]) -> float:
        """Calculate recent success rate for a task (last 10 attempts)"""
        if not history:
            return 0.0
            
        recent_results = history[-10:]  # Last 10 attempts
        successes = sum(1 for result in recent_results if result.get('success', False))
        
        return successes / len(recent_results)
    
    def update_task_history(self, task_name: str, result: Dict[str, Any]):
        """Update performance history for a task"""
        if task_name not in self.task_history:
            self.task_history[task_name] = []
            
        self.task_history[task_name].append({
            'success': result.get('success', False),
            'reward': result.get('reward', 0.0),
            'steps': result.get('steps_taken', 0),
            'timestamp': result.get('timestamp', ''),
        })
        
        # Keep only last 50 results to manage memory
        self.task_history[task_name] = self.task_history[task_name][-50:]
    
    def get_phase_statistics(self, phase: TrainingPhase) -> Dict[str, Any]:
        """Get statistics for tasks in a specific phase"""
        tasks = self.phase_tasks.get(phase, [])
        
        if not tasks:
            return {}
        
        total_tasks = len(tasks)
        attempted_tasks = len([t for t in tasks if t in self.task_history])
        
        # Calculate average success rate for attempted tasks
        success_rates = []
        for task_name in tasks:
            if task_name in self.task_history:
                rate = self._calculate_recent_success_rate(self.task_history[task_name])
                success_rates.append(rate)
        
        avg_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0.0
        
        return {
            'phase': phase.value,
            'total_tasks': total_tasks,
            'attempted_tasks': attempted_tasks,
            'avg_success_rate': avg_success_rate,
            'completion_percentage': attempted_tasks / total_tasks * 100,
        }