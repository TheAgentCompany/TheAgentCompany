#!/usr/bin/env python3
"""
TAC-RL Training Monitor
=======================

Monitoring script for viewing training progress, generating reports,
and analyzing performance metrics.

Usage:
    python monitor.py --run-id latest
    python monitor.py --logs-dir ./logs --generate-report
    python monitor.py --visualize --output-dir ./plots
"""

import os
import sys
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time

# Add the tac_rl directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Optional imports for rich console output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.live import Live
    from rich.layout import Layout
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# Optional imports for visualization
try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    HAS_VISUALIZATION = True
except ImportError:
    HAS_VISUALIZATION = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingMonitorCLI:
    """CLI tool for monitoring TAC-RL training"""
    
    def __init__(self, logs_dir: str = "./logs"):
        self.logs_dir = Path(logs_dir)
        self.console = Console() if HAS_RICH else None
        
        # Find available runs
        self.available_runs = self._find_available_runs()
        
    def _find_available_runs(self) -> List[Dict[str, Any]]:
        """Find available training runs"""
        
        runs = []
        
        if not self.logs_dir.exists():
            return runs
            
        # Look for training_metrics.jsonl files
        for log_path in self.logs_dir.glob("**/training_metrics.jsonl"):
            try:
                # Read first line to get start info
                with open(log_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        first_metric = json.loads(first_line)
                        
                        # Count total iterations
                        total_iterations = sum(1 for _ in open(log_path, 'r'))
                        
                        runs.append({
                            'path': log_path.parent,
                            'name': log_path.parent.name,
                            'start_time': first_metric.get('timestamp', 'unknown'),
                            'total_iterations': total_iterations,
                            'last_modified': datetime.fromtimestamp(log_path.stat().st_mtime)
                        })
                        
            except Exception as e:
                logger.debug(f"Error reading {log_path}: {e}")
                
        # Sort by last modified (most recent first)
        runs.sort(key=lambda x: x['last_modified'], reverse=True)
        
        return runs
    
    def show_available_runs(self):
        """Display available training runs"""
        
        if not self.available_runs:
            print("No training runs found.")
            return
            
        if HAS_RICH and self.console:
            table = Table(title="Available Training Runs")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Start Time", style="yellow")
            table.add_column("Iterations", justify="right")
            table.add_column("Last Modified", style="blue")
            
            for i, run in enumerate(self.available_runs):
                table.add_row(
                    str(i),
                    run['name'],
                    run['start_time'][:19] if len(run['start_time']) > 19 else run['start_time'],
                    str(run['total_iterations']),
                    run['last_modified'].strftime("%Y-%m-%d %H:%M")
                )
                
            self.console.print(table)
        else:
            print("\nAvailable Training Runs:")
            print("-" * 60)
            for i, run in enumerate(self.available_runs):
                print(f"{i}: {run['name']} - {run['total_iterations']} iterations")
    
    def monitor_run(self, run_id: str = "latest", watch: bool = False):
        """Monitor a specific training run"""
        
        if run_id == "latest" and self.available_runs:
            run = self.available_runs[0]
        elif run_id.isdigit() and int(run_id) < len(self.available_runs):
            run = self.available_runs[int(run_id)]
        else:
            # Try to find by name
            matching_runs = [r for r in self.available_runs if run_id in r['name']]
            if matching_runs:
                run = matching_runs[0]
            else:
                print(f"Run not found: {run_id}")
                return
        
        print(f"Monitoring run: {run['name']}")
        print(f"Path: {run['path']}")
        
        if watch:
            self._watch_training(run)
        else:
            self._show_run_summary(run)
    
    def _watch_training(self, run: Dict[str, Any]):
        """Watch training progress in real-time"""
        
        metrics_file = run['path'] / 'training_metrics.jsonl'
        
        if not HAS_RICH:
            print("Real-time monitoring requires 'rich' library. Install with: pip install rich")
            return
        
        with Live(self._create_live_display(run), refresh_per_second=1) as live:
            last_size = 0
            
            while True:
                try:
                    if metrics_file.exists():
                        current_size = metrics_file.stat().st_size
                        
                        if current_size != last_size:
                            live.update(self._create_live_display(run))
                            last_size = current_size
                    
                    time.sleep(2)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Error in watch mode: {e}")
                    break
    
    def _create_live_display(self, run: Dict[str, Any]) -> Layout:
        """Create live display layout for monitoring"""
        
        layout = Layout()
        
        # Load latest metrics
        metrics = self._load_latest_metrics(run)
        
        # Create panels
        if metrics:
            stats_panel = self._create_stats_panel(metrics)
            progress_panel = self._create_progress_panel(run)
            
            layout.split_column(
                Layout(stats_panel, size=10),
                Layout(progress_panel, size=6)
            )
        else:
            layout.update(Panel("No metrics available", title="Training Monitor"))
        
        return layout
    
    def _create_stats_panel(self, metrics: Dict[str, Any]) -> Panel:
        """Create statistics panel"""
        
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="green", width=15)
        
        table.add_row("Iteration", str(metrics.get('iteration', 'N/A')))
        table.add_row("Phase", metrics.get('phase', 'N/A'))
        table.add_row("Success Rate", f"{metrics.get('success_rate', 0):.3f}")
        table.add_row("Mean Reward", f"{metrics.get('mean_reward', 0):.3f}")
        table.add_row("Batch Size", str(metrics.get('batch_size', 'N/A')))
        table.add_row("Mean Steps", f"{metrics.get('mean_steps', 0):.1f}")
        
        return Panel(table, title="Current Statistics", border_style="blue")
    
    def _create_progress_panel(self, run: Dict[str, Any]) -> Panel:
        """Create progress panel"""
        
        # Load all metrics to calculate progress
        all_metrics = self._load_all_metrics(run)
        
        if not all_metrics:
            return Panel("No progress data", title="Progress")
        
        # Calculate phase distribution
        phase_counts = {}
        for metric in all_metrics:
            phase = metric.get('phase', 'unknown')
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        table = Table(show_header=True, box=None)
        table.add_column("Phase", style="yellow")
        table.add_column("Iterations", justify="right")
        
        for phase, count in phase_counts.items():
            table.add_row(phase.title(), str(count))
        
        return Panel(table, title="Phase Progress", border_style="green")
    
    def _load_latest_metrics(self, run: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Load latest metrics from run"""
        
        metrics_file = run['path'] / 'training_metrics.jsonl'
        
        if not metrics_file.exists():
            return None
        
        try:
            # Read last line
            with open(metrics_file, 'rb') as f:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
                last_line = f.readline().decode()
                
            return json.loads(last_line.strip())
            
        except Exception as e:
            logger.debug(f"Error loading latest metrics: {e}")
            return None
    
    def _load_all_metrics(self, run: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load all metrics from run"""
        
        metrics_file = run['path'] / 'training_metrics.jsonl'
        
        if not metrics_file.exists():
            return []
        
        try:
            metrics = []
            with open(metrics_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        metrics.append(json.loads(line))
            return metrics
            
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            return []
    
    def _show_run_summary(self, run: Dict[str, Any]):
        """Show summary of a training run"""
        
        metrics = self._load_all_metrics(run)
        
        if not metrics:
            print("No metrics available for this run.")
            return
        
        # Calculate summary statistics
        total_iterations = len(metrics)
        latest_metrics = metrics[-1] if metrics else {}
        
        # Success rate progression
        success_rates = [m.get('success_rate', 0) for m in metrics]
        best_success_rate = max(success_rates) if success_rates else 0
        current_success_rate = success_rates[-1] if success_rates else 0
        
        # Reward progression
        rewards = [m.get('mean_reward', 0) for m in metrics]
        best_reward = max(rewards) if rewards else 0
        current_reward = rewards[-1] if rewards else 0
        
        # Phase distribution
        phases = [m.get('phase', 'unknown') for m in metrics]
        current_phase = phases[-1] if phases else 'unknown'
        
        if HAS_RICH and self.console:
            # Create summary table
            table = Table(title=f"Training Run Summary: {run['name']}")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Iterations", str(total_iterations))
            table.add_row("Current Phase", current_phase)
            table.add_row("Current Success Rate", f"{current_success_rate:.3f}")
            table.add_row("Best Success Rate", f"{best_success_rate:.3f}")
            table.add_row("Current Mean Reward", f"{current_reward:.3f}")
            table.add_row("Best Mean Reward", f"{best_reward:.3f}")
            table.add_row("Start Time", run['start_time'])
            table.add_row("Last Modified", run['last_modified'].strftime("%Y-%m-%d %H:%M:%S"))
            
            self.console.print(table)
        else:
            print(f"\nTraining Run Summary: {run['name']}")
            print("-" * 40)
            print(f"Total Iterations: {total_iterations}")
            print(f"Current Phase: {current_phase}")
            print(f"Current Success Rate: {current_success_rate:.3f}")
            print(f"Best Success Rate: {best_success_rate:.3f}")
            print(f"Current Mean Reward: {current_reward:.3f}")
            print(f"Best Mean Reward: {best_reward:.3f}")
    
    def generate_report(self, run_id: str = "latest", output_file: Optional[str] = None):
        """Generate detailed training report"""
        
        if run_id == "latest" and self.available_runs:
            run = self.available_runs[0]
        elif run_id.isdigit() and int(run_id) < len(self.available_runs):
            run = self.available_runs[int(run_id)]
        else:
            print(f"Run not found: {run_id}")
            return
        
        metrics = self._load_all_metrics(run)
        
        if not metrics:
            print("No metrics available for report generation.")
            return
        
        # Generate report
        report = self._create_detailed_report(run, metrics)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        else:
            print(report)
    
    def _create_detailed_report(self, run: Dict[str, Any], metrics: List[Dict[str, Any]]) -> str:
        """Create detailed training report"""
        
        report = []
        report.append(f"# TAC-RL Training Report")
        report.append(f"")
        report.append(f"**Run**: {run['name']}")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"")
        
        # Overall statistics
        report.append("## Overall Statistics")
        report.append("")
        
        total_iterations = len(metrics)
        success_rates = [m.get('success_rate', 0) for m in metrics]
        rewards = [m.get('mean_reward', 0) for m in metrics]
        
        report.append(f"- **Total Iterations**: {total_iterations}")
        report.append(f"- **Best Success Rate**: {max(success_rates):.3f}")
        report.append(f"- **Final Success Rate**: {success_rates[-1]:.3f}")
        report.append(f"- **Best Mean Reward**: {max(rewards):.3f}")
        report.append(f"- **Final Mean Reward**: {rewards[-1]:.3f}")
        report.append("")
        
        # Phase progression
        report.append("## Phase Progression")
        report.append("")
        
        phase_stats = {}
        for metric in metrics:
            phase = metric.get('phase', 'unknown')
            if phase not in phase_stats:
                phase_stats[phase] = []
            phase_stats[phase].append(metric)
        
        for phase, phase_metrics in phase_stats.items():
            phase_success_rates = [m.get('success_rate', 0) for m in phase_metrics]
            avg_success_rate = sum(phase_success_rates) / len(phase_success_rates)
            
            report.append(f"- **{phase.title()}**: {len(phase_metrics)} iterations, avg success rate: {avg_success_rate:.3f}")
        
        report.append("")
        
        # Recent performance
        recent_metrics = metrics[-10:]  # Last 10 iterations
        report.append("## Recent Performance (Last 10 Iterations)")
        report.append("")
        
        for metric in recent_metrics:
            iteration = metric.get('iteration', 'N/A')
            success_rate = metric.get('success_rate', 0)
            mean_reward = metric.get('mean_reward', 0)
            phase = metric.get('phase', 'unknown')
            
            report.append(f"- Iteration {iteration} [{phase}]: success_rate={success_rate:.3f}, mean_reward={mean_reward:.3f}")
        
        return "\n".join(report)
    
    def visualize(self, run_id: str = "latest", output_dir: str = "./plots"):
        """Generate training visualizations"""
        
        if not HAS_VISUALIZATION:
            print("Visualization requires matplotlib and seaborn. Install with: pip install matplotlib seaborn pandas")
            return
        
        if run_id == "latest" and self.available_runs:
            run = self.available_runs[0]
        else:
            print(f"Run not found: {run_id}")
            return
        
        metrics = self._load_all_metrics(run)
        
        if not metrics:
            print("No metrics available for visualization.")
            return
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Convert to DataFrame
        df = pd.DataFrame(metrics)
        
        # Create visualizations
        self._create_training_plots(df, output_path, run['name'])
        
        print(f"Visualizations saved to: {output_path}")
    
    def _create_training_plots(self, df: pd.DataFrame, output_path: Path, run_name: str):
        """Create training visualization plots"""
        
        plt.style.use('seaborn-v0_8')
        
        # Plot 1: Success rate and reward over time
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        ax1.plot(df['iteration'], df['success_rate'], linewidth=2, label='Success Rate')
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Success Rate')
        ax1.set_title(f'Training Progress - {run_name}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.plot(df['iteration'], df['mean_reward'], linewidth=2, color='orange', label='Mean Reward')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Mean Reward')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(output_path / 'training_progress.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Plot 2: Phase performance
        if 'phase' in df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            phase_performance = df.groupby('phase')['success_rate'].agg(['mean', 'std', 'count'])
            
            x = range(len(phase_performance))
            ax.bar(x, phase_performance['mean'], yerr=phase_performance['std'], 
                   capsize=5, alpha=0.7)
            ax.set_xlabel('Training Phase')
            ax.set_ylabel('Mean Success Rate')
            ax.set_title('Performance by Training Phase')
            ax.set_xticks(x)
            ax.set_xticklabels(phase_performance.index, rotation=45)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(output_path / 'phase_performance.png', dpi=300, bbox_inches='tight')
            plt.close()

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="TAC-RL Training Monitor")
    parser.add_argument('--logs-dir', type=str, default='./logs', help='Logs directory path')
    parser.add_argument('--run-id', type=str, default='latest', help='Training run ID to monitor')
    parser.add_argument('--list', action='store_true', help='List available training runs')
    parser.add_argument('--watch', action='store_true', help='Watch training progress in real-time')
    parser.add_argument('--generate-report', action='store_true', help='Generate detailed report')
    parser.add_argument('--report-output', type=str, help='Output file for report')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    parser.add_argument('--output-dir', type=str, default='./plots', help='Output directory for visualizations')
    
    args = parser.parse_args()
    
    # Create monitor
    monitor = TrainingMonitorCLI(args.logs_dir)
    
    if args.list:
        monitor.show_available_runs()
    elif args.generate_report:
        monitor.generate_report(args.run_id, args.report_output)
    elif args.visualize:
        monitor.visualize(args.run_id, args.output_dir)
    else:
        monitor.monitor_run(args.run_id, args.watch)

if __name__ == "__main__":
    main()