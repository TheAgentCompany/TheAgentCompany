"""
Training Monitoring and Logging System for TAC-RL
=================================================

Comprehensive monitoring, logging, and visualization system for 
tracking training progress, performance metrics, and debugging.
"""

import logging
import json
import os
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import threading

# Optional imports for visualization
try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    HAS_VISUALIZATION = True
except ImportError:
    HAS_VISUALIZATION = False

try:
    import wandb
    HAS_WANDB = True
except ImportError:
    HAS_WANDB = False

from ..architecture import TrainingResult, TrainingConfig, TrainingPhase

@dataclass
class TrainingMetrics:
    """Training metrics for a single iteration"""
    iteration: int
    timestamp: str
    phase: str
    batch_size: int
    
    # Task performance
    success_rate: float
    mean_reward: float
    median_reward: float
    max_reward: float
    min_reward: float
    
    # Efficiency metrics
    mean_steps: float
    mean_execution_time: float
    
    # Learning metrics
    loss: Optional[float] = None
    policy_loss: Optional[float] = None
    value_loss: Optional[float] = None
    learning_rate: Optional[float] = None
    
    # Domain breakdown
    domain_performance: Dict[str, float] = None

class TrainingMonitor:
    """Comprehensive training monitoring system"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Setup logging directories
        self.log_dir = Path(config.log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging files
        self.metrics_file = self.log_dir / "training_metrics.jsonl"
        self.results_file = self.log_dir / "task_results.jsonl"
        self.events_file = self.log_dir / "training_events.log"
        
        # Setup file logging
        self._setup_file_logging()
        
        # Initialize WandB if available and configured
        self.wandb_run = None
        if HAS_WANDB and config.monitoring.get('use_wandb', False):
            self._setup_wandb()
        
        # Training state tracking
        self.iteration_count = 0
        self.start_time = datetime.now()
        self.phase_start_time = datetime.now()
        
        # Metrics history
        self.metrics_history: List[TrainingMetrics] = []
        self.results_history: List[TrainingResult] = []
        
        # Performance tracking
        self.best_success_rate = 0.0
        self.best_mean_reward = 0.0
        self.consecutive_improvements = 0
        
        # Real-time monitoring
        self.enable_realtime = config.monitoring.get('realtime_monitoring', True)
        self.monitoring_thread = None
        self.should_monitor = True
        
        if self.enable_realtime:
            self._start_realtime_monitoring()
    
    def _setup_file_logging(self):
        """Setup file-based logging"""
        
        # Create file handler for training events
        file_handler = logging.FileHandler(self.events_file)
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Add to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        
        self.logger.info(f"File logging setup complete: {self.events_file}")
    
    def _setup_wandb(self):
        """Setup Weights & Biases integration"""
        
        if not HAS_WANDB:
            self.logger.warning("WandB requested but not available")
            return
        
        try:
            project_name = self.config.monitoring.get('project_name', 'tac-rl-training')
            
            self.wandb_run = wandb.init(
                project=project_name,
                name=f"tac-rl-{self.config.model.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                config={
                    'model': asdict(self.config.model),
                    'training': asdict(self.config),
                    'start_time': self.start_time.isoformat()
                }
            )
            
            self.logger.info(f"WandB initialized: {project_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WandB: {e}")
            self.wandb_run = None
    
    def _start_realtime_monitoring(self):
        """Start real-time monitoring thread"""
        
        def monitoring_loop():
            while self.should_monitor:
                try:
                    self._update_realtime_metrics()
                    time.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(60)  # Wait longer on error
        
        self.monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info("Real-time monitoring started")
    
    def log_iteration(self, results: List[TrainingResult], rewards: List[float]):
        """Log results from a training iteration"""
        
        self.iteration_count += 1
        
        try:
            # Calculate metrics
            metrics = self._calculate_metrics(results, rewards)
            
            # Store in history
            self.metrics_history.append(metrics)
            self.results_history.extend(results)
            
            # Write to files
            self._write_metrics_to_file(metrics)
            self._write_results_to_file(results)
            
            # Log to WandB
            if self.wandb_run:
                self._log_to_wandb(metrics, results)
            
            # Update performance tracking
            self._update_performance_tracking(metrics)
            
            # Console logging
            self._log_to_console(metrics)
            
            # Generate periodic reports
            if self.iteration_count % 10 == 0:
                self._generate_progress_report()
            
            self.logger.info(f"Logged iteration {self.iteration_count} with {len(results)} tasks")
            
        except Exception as e:
            self.logger.error(f"Failed to log iteration {self.iteration_count}: {e}", exc_info=True)
    
    def _calculate_metrics(self, results: List[TrainingResult], rewards: List[float]) -> TrainingMetrics:
        """Calculate metrics from training results"""
        
        if not results:
            return TrainingMetrics(
                iteration=self.iteration_count,
                timestamp=datetime.now().isoformat(),
                phase=self.config.current_phase.value,
                batch_size=0,
                success_rate=0.0,
                mean_reward=0.0,
                median_reward=0.0,
                max_reward=0.0,
                min_reward=0.0,
                mean_steps=0.0,
                mean_execution_time=0.0
            )
        
        # Basic metrics
        success_rate = sum(1 for r in results if r.success) / len(results)
        mean_reward = sum(rewards) / len(rewards)
        median_reward = sorted(rewards)[len(rewards) // 2]
        max_reward = max(rewards)
        min_reward = min(rewards)
        
        mean_steps = sum(r.steps_taken for r in results) / len(results)
        mean_execution_time = sum(r.execution_time for r in results) / len(results)
        
        # Domain breakdown
        domain_performance = self._calculate_domain_performance(results)
        
        return TrainingMetrics(
            iteration=self.iteration_count,
            timestamp=datetime.now().isoformat(),
            phase=self.config.current_phase.value,
            batch_size=len(results),
            success_rate=success_rate,
            mean_reward=mean_reward,
            median_reward=median_reward,
            max_reward=max_reward,
            min_reward=min_reward,
            mean_steps=mean_steps,
            mean_execution_time=mean_execution_time,
            domain_performance=domain_performance
        )
    
    def _calculate_domain_performance(self, results: List[TrainingResult]) -> Dict[str, float]:
        """Calculate performance breakdown by domain"""
        
        domain_results = {}
        
        for result in results:
            domain = self._infer_domain_from_task_name(result.task_name)
            if domain not in domain_results:
                domain_results[domain] = {'total': 0, 'success': 0}
            
            domain_results[domain]['total'] += 1
            if result.success:
                domain_results[domain]['success'] += 1
        
        # Calculate success rates
        domain_performance = {}
        for domain, stats in domain_results.items():
            if stats['total'] > 0:
                domain_performance[domain] = stats['success'] / stats['total']
        
        return domain_performance
    
    def _infer_domain_from_task_name(self, task_name: str) -> str:
        """Infer domain from task name"""
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
    
    def _write_metrics_to_file(self, metrics: TrainingMetrics):
        """Write metrics to JSONL file"""
        
        with open(self.metrics_file, 'a') as f:
            json.dump(asdict(metrics), f)
            f.write('\n')
    
    def _write_results_to_file(self, results: List[TrainingResult]):
        """Write individual results to JSONL file"""
        
        with open(self.results_file, 'a') as f:
            for result in results:
                json.dump(asdict(result), f)
                f.write('\n')
    
    def _log_to_wandb(self, metrics: TrainingMetrics, results: List[TrainingResult]):
        """Log metrics to Weights & Biases"""
        
        if not self.wandb_run:
            return
        
        try:
            log_data = {
                'iteration': metrics.iteration,
                'phase': metrics.phase,
                'success_rate': metrics.success_rate,
                'mean_reward': metrics.mean_reward,
                'median_reward': metrics.median_reward,
                'max_reward': metrics.max_reward,
                'min_reward': metrics.min_reward,
                'mean_steps': metrics.mean_steps,
                'mean_execution_time': metrics.mean_execution_time,
                'batch_size': metrics.batch_size,
            }
            
            # Add domain performance
            if metrics.domain_performance:
                for domain, perf in metrics.domain_performance.items():
                    log_data[f'domain_{domain}_success_rate'] = perf
            
            # Add training metrics if available
            if metrics.loss is not None:
                log_data['loss'] = metrics.loss
            if metrics.policy_loss is not None:
                log_data['policy_loss'] = metrics.policy_loss
            if metrics.value_loss is not None:
                log_data['value_loss'] = metrics.value_loss
            if metrics.learning_rate is not None:
                log_data['learning_rate'] = metrics.learning_rate
            
            self.wandb_run.log(log_data)
            
        except Exception as e:
            self.logger.error(f"Failed to log to WandB: {e}")
    
    def _update_performance_tracking(self, metrics: TrainingMetrics):
        """Update performance tracking metrics"""
        
        # Track best performance
        if metrics.success_rate > self.best_success_rate:
            self.best_success_rate = metrics.success_rate
            self.consecutive_improvements += 1
        else:
            self.consecutive_improvements = 0
        
        if metrics.mean_reward > self.best_mean_reward:
            self.best_mean_reward = metrics.mean_reward
    
    def _log_to_console(self, metrics: TrainingMetrics):
        """Log metrics to console"""
        
        self.logger.info(
            f"Iteration {metrics.iteration} [{metrics.phase}]: "
            f"success_rate={metrics.success_rate:.3f}, "
            f"mean_reward={metrics.mean_reward:.3f}, "
            f"mean_steps={metrics.mean_steps:.1f}, "
            f"batch_size={metrics.batch_size}"
        )
        
        # Log domain breakdown
        if metrics.domain_performance:
            domain_str = ", ".join([
                f"{domain}={perf:.3f}" 
                for domain, perf in metrics.domain_performance.items()
            ])
            self.logger.info(f"Domain performance: {domain_str}")
    
    def _update_realtime_metrics(self):
        """Update real-time monitoring metrics"""
        
        if not self.metrics_history:
            return
        
        current_time = datetime.now()
        
        # Calculate training speed
        elapsed_time = (current_time - self.start_time).total_seconds()
        iterations_per_hour = (self.iteration_count / elapsed_time) * 3600 if elapsed_time > 0 else 0
        
        # Log real-time stats
        self.logger.debug(
            f"Real-time: {self.iteration_count} iterations in {elapsed_time/3600:.2f}h, "
            f"speed={iterations_per_hour:.1f} iter/h, "
            f"best_success_rate={self.best_success_rate:.3f}"
        )
    
    def _generate_progress_report(self):
        """Generate detailed progress report"""
        
        if not self.metrics_history:
            return
        
        report_file = self.log_dir / f"progress_report_iter_{self.iteration_count}.md"
        
        try:
            with open(report_file, 'w') as f:
                f.write(f"# TAC-RL Training Progress Report\n\n")
                f.write(f"**Report Generated**: {datetime.now().isoformat()}\n\n")
                
                # Overall statistics
                f.write("## Overall Statistics\n\n")
                f.write(f"- **Iterations Completed**: {self.iteration_count}\n")
                f.write(f"- **Current Phase**: {self.config.current_phase.value}\n")
                f.write(f"- **Best Success Rate**: {self.best_success_rate:.3f}\n")
                f.write(f"- **Best Mean Reward**: {self.best_mean_reward:.3f}\n")
                f.write(f"- **Consecutive Improvements**: {self.consecutive_improvements}\n\n")
                
                # Recent performance
                recent_metrics = self.metrics_history[-5:]  # Last 5 iterations
                if recent_metrics:
                    f.write("## Recent Performance (Last 5 Iterations)\n\n")
                    for m in recent_metrics:
                        f.write(f"- Iteration {m.iteration}: success_rate={m.success_rate:.3f}, mean_reward={m.mean_reward:.3f}\n")
                    f.write("\n")
                
                # Phase progression
                f.write("## Phase Progression\n\n")
                phase_stats = self._calculate_phase_statistics()
                for phase, stats in phase_stats.items():
                    f.write(f"- **{phase}**: {stats}\n")
                
            self.logger.info(f"Progress report generated: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate progress report: {e}")
    
    def _calculate_phase_statistics(self) -> Dict[str, str]:
        """Calculate statistics for each training phase"""
        
        phase_stats = {}
        
        for phase in TrainingPhase:
            phase_metrics = [m for m in self.metrics_history if m.phase == phase.value]
            
            if phase_metrics:
                avg_success = sum(m.success_rate for m in phase_metrics) / len(phase_metrics)
                avg_reward = sum(m.mean_reward for m in phase_metrics) / len(phase_metrics)
                phase_stats[phase.value] = f"{len(phase_metrics)} iterations, avg_success={avg_success:.3f}, avg_reward={avg_reward:.3f}"
            else:
                phase_stats[phase.value] = "Not started"
        
        return phase_stats
    
    def generate_visualizations(self):
        """Generate training visualizations"""
        
        if not HAS_VISUALIZATION or not self.metrics_history:
            self.logger.warning("Visualization not available or no data")
            return
        
        try:
            # Create visualizations directory
            viz_dir = self.log_dir / "visualizations"
            viz_dir.mkdir(exist_ok=True)
            
            # Convert metrics to DataFrame
            df = pd.DataFrame([asdict(m) for m in self.metrics_history])
            
            # Plot 1: Success rate over time
            plt.figure(figsize=(12, 6))
            plt.subplot(2, 2, 1)
            plt.plot(df['iteration'], df['success_rate'])
            plt.title('Success Rate Over Time')
            plt.xlabel('Iteration')
            plt.ylabel('Success Rate')
            plt.grid(True)
            
            # Plot 2: Mean reward over time
            plt.subplot(2, 2, 2)
            plt.plot(df['iteration'], df['mean_reward'])
            plt.title('Mean Reward Over Time')
            plt.xlabel('Iteration')
            plt.ylabel('Mean Reward')
            plt.grid(True)
            
            # Plot 3: Efficiency metrics
            plt.subplot(2, 2, 3)
            plt.plot(df['iteration'], df['mean_steps'], label='Mean Steps')
            plt.plot(df['iteration'], df['mean_execution_time'], label='Mean Time (s)')
            plt.title('Efficiency Metrics')
            plt.xlabel('Iteration')
            plt.ylabel('Value')
            plt.legend()
            plt.grid(True)
            
            # Plot 4: Phase performance
            plt.subplot(2, 2, 4)
            phase_data = df.groupby('phase')['success_rate'].mean()
            plt.bar(phase_data.index, phase_data.values)
            plt.title('Success Rate by Phase')
            plt.xlabel('Phase')
            plt.ylabel('Mean Success Rate')
            plt.xticks(rotation=45)
            plt.grid(True)
            
            plt.tight_layout()
            plt.savefig(viz_dir / 'training_progress.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Visualizations saved to {viz_dir}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate visualizations: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current training status"""
        
        return {
            'iteration_count': self.iteration_count,
            'current_phase': self.config.current_phase.value,
            'best_success_rate': self.best_success_rate,
            'best_mean_reward': self.best_mean_reward,
            'consecutive_improvements': self.consecutive_improvements,
            'total_tasks_processed': len(self.results_history),
            'elapsed_time': str(datetime.now() - self.start_time),
            'log_dir': str(self.log_dir)
        }
    
    def cleanup(self):
        """Clean up monitoring resources"""
        
        self.should_monitor = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
        
        if self.wandb_run:
            try:
                self.wandb_run.finish()
            except:
                pass
        
        self.logger.info("Training monitor cleanup complete")