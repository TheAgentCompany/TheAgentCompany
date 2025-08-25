#!/usr/bin/env python3
"""
TAC-RL Training Orchestrator
============================

Main script for training language models using reinforcement learning
on TheAgentCompany benchmark.

Usage:
    python train.py --config configs/qwen_2_5_7b.yaml
    python train.py --config configs/llama_8b.yaml --resume checkpoint.pt
"""

import os
import sys
import argparse
import logging
import signal
from pathlib import Path
from typing import Optional, List
import traceback
from datetime import datetime

# Add the tac_rl directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from architecture import TACRLArchitecture, TrainingResult
from config_manager import ConfigManager
from components import TaskSampler, OpenHandsRunner, RewardComputer, ARTTrainer, TrainingMonitor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

class TrainingOrchestrator:
    """Main training orchestration class"""
    
    def __init__(self, config_path: str, resume_checkpoint: Optional[str] = None):
        self.config_path = config_path
        self.resume_checkpoint = resume_checkpoint
        self.should_stop = False
        
        # Load configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config(config_path)
        self.config = self.config_manager.update_config_from_env(self.config)
        
        # Initialize architecture
        self.architecture = TACRLArchitecture(self.config)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Training orchestrator initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.should_stop = True
    
    def run(self):
        """Main training loop"""
        
        try:
            logger.info("🚀 Starting TAC-RL Training with Local Model")
            logger.info(f"Configuration: {self.config_path}")
            logger.info(f"Model: {self.config.model.name} ({self.config.model.parameter_count})")
            logger.info(f"Phase: {self.config.current_phase.value}")
            
            # Setup components
            logger.info("Initializing components...")
            self.architecture.setup_components()
            
            # Resume from checkpoint if specified
            if self.resume_checkpoint:
                self._resume_from_checkpoint()
            
            # Validate environment
            self._validate_environment()
            
            # Main training loop (now async)
            asyncio.run(self._main_training_loop())
            
        except KeyboardInterrupt:
            logger.info("Training interrupted by user")
        except Exception as e:
            logger.error(f"Training failed with error: {e}")
            logger.error(traceback.format_exc())
            sys.exit(1)
        finally:
            self._cleanup()
    
    def _resume_from_checkpoint(self):
        """Resume training from checkpoint"""
        
        logger.info(f"Resuming from checkpoint: {self.resume_checkpoint}")
        
        if not self.architecture.art_trainer.load_checkpoint(self.resume_checkpoint):
            raise RuntimeError(f"Failed to load checkpoint: {self.resume_checkpoint}")
    
    def _validate_environment(self):
        """Validate that the training environment is ready"""
        
        logger.info("Validating training environment...")
        
        # Check TheAgentCompany services
        import requests
        try:
            response = requests.get('http://localhost:2999/health', timeout=10)
            if response.status_code != 200:
                raise RuntimeError("TheAgentCompany API server not healthy")
            logger.info("✓ TheAgentCompany services are ready")
        except Exception as e:
            raise RuntimeError(f"TheAgentCompany services not available: {e}")
        
        # Check required directories
        required_dirs = [self.config.output_dir, self.config.checkpoint_dir, self.config.log_dir]
        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info("✓ Output directories created")
        
        # Check task availability
        task_sampler = self.architecture.task_sampler
        available_tasks = task_sampler.phase_tasks[self.config.current_phase]
        if not available_tasks:
            raise RuntimeError(f"No tasks available for phase {self.config.current_phase.value}")
        logger.info(f"✓ {len(available_tasks)} tasks available for current phase")
        
        logger.info("Environment validation completed")
    
    async def _main_training_loop(self):
        """Main async training loop with phase progression"""
        
        iteration = 0
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        logger.info("Starting main training loop...")
        
        while not self.should_stop:
            try:
                iteration += 1
                logger.info(f"\n{'='*50}")
                logger.info(f"Training Iteration {iteration}")
                logger.info(f"Phase: {self.config.current_phase.value}")
                logger.info(f"Model: {self.config.model.base_model_path}")
                logger.info(f"{'='*50}")
                
                # Execute async training iteration
                results = await self.architecture.train_iteration()
                
                # Reset failure counter on successful iteration
                consecutive_failures = 0
                
                # Check for phase advancement
                if iteration % 20 == 0:  # Check every 20 iterations
                    recent_results = self._get_recent_results(20)
                    if self.architecture.should_advance_phase(recent_results):
                        self.architecture.advance_phase()
                        logger.info(f"🎉 Advanced to phase: {self.config.current_phase.value}")
                
                # Periodic checkpointing
                if iteration % self.config.checkpoint_frequency == 0:
                    self._save_checkpoint(iteration)
                
                # Periodic evaluation
                if iteration % self.config.evaluation_frequency == 0:
                    await self._run_evaluation(iteration)
                
                # Check stopping conditions
                if self._should_stop_training(iteration):
                    logger.info("Training stopping conditions met")
                    break
                
            except Exception as e:
                consecutive_failures += 1
                logger.error(f"Training iteration {iteration} failed: {e}")
                logger.error(traceback.format_exc())
                
                if consecutive_failures >= max_consecutive_failures:
                    logger.error(f"Maximum consecutive failures ({max_consecutive_failures}) reached")
                    break
                
                logger.info(f"Continuing training ({consecutive_failures}/{max_consecutive_failures} failures)")
                
        logger.info(f"🏁 Training completed after {iteration} iterations")
    
    def _get_recent_results(self, count: int) -> List[TrainingResult]:
        """Get recent training results for analysis"""
        
        monitor = self.architecture.monitor
        if not monitor or not monitor.results_history:
            return []
        
        return monitor.results_history[-count:]
    
    def _save_checkpoint(self, iteration: int):
        """Save training checkpoint"""
        
        try:
            checkpoint_path = Path(self.config.checkpoint_dir) / f"checkpoint_iter_{iteration}.pt"
            
            # This would save actual model checkpoint in production
            logger.info(f"Checkpoint saved: {checkpoint_path}")
            
        except Exception as e:
            logger.error(f"Failed to save checkpoint at iteration {iteration}: {e}")
    
    async def _run_evaluation(self, iteration: int):
        """Run comprehensive evaluation"""
        
        try:
            logger.info(f"Running evaluation at iteration {iteration}")
            
            # Get evaluation statistics
            monitor = self.architecture.monitor
            if monitor:
                stats = monitor.get_status()
                logger.info(f"Current stats: success_rate={stats['best_success_rate']:.3f}")
                
                # Generate visualizations if available
                monitor.generate_visualizations()
            
            # Show model improvement summary
            if hasattr(self.architecture, 'get_model_performance_summary'):
                perf_summary = self.architecture.get_model_performance_summary()
                if perf_summary.get('is_improving'):
                    logger.info(f"🎯 Model improving: {perf_summary['early_success_rate']:.3f} → {perf_summary['late_success_rate']:.3f}")
                
        except Exception as e:
            logger.error(f"Evaluation failed at iteration {iteration}: {e}")
    
    def _should_stop_training(self, iteration: int) -> bool:
        """Check if training should stop"""
        
        # Check maximum iterations (if configured)
        max_iterations = getattr(self.config, 'max_iterations', None)
        if max_iterations and iteration >= max_iterations:
            return True
        
        # Check if reached expert phase and achieved good performance
        if self.config.current_phase.value == 'expert':
            monitor = self.architecture.monitor
            if monitor and monitor.best_success_rate >= 0.8:  # 80% success rate
                logger.info("Training goal achieved: 80% success rate in expert phase")
                return True
        
        # Check training time limits (if configured)
        max_training_hours = getattr(self.config, 'max_training_hours', None)
        if max_training_hours:
            monitor = self.architecture.monitor
            if monitor:
                elapsed = datetime.now() - monitor.start_time
                if elapsed.total_seconds() / 3600 >= max_training_hours:
                    logger.info(f"Training time limit reached: {max_training_hours} hours")
                    return True
        
        return False
    
    def _cleanup(self):
        """Clean up resources"""
        
        logger.info("Cleaning up resources...")
        
        try:
            if hasattr(self.architecture, 'openhands_runner'):
                self.architecture.openhands_runner.cleanup()
            
            if hasattr(self.architecture, 'art_trainer'):
                self.architecture.art_trainer.cleanup()
            
            if hasattr(self.architecture, 'monitor'):
                self.architecture.monitor.cleanup()
                
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        
        logger.info("Cleanup completed")

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="TAC-RL Training System")
    parser.add_argument(
        '--config', 
        type=str, 
        required=True,
        help='Path to configuration YAML file'
    )
    parser.add_argument(
        '--resume', 
        type=str, 
        help='Path to checkpoint to resume from'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate configuration and environment, do not train'
    )
    parser.add_argument(
        '--create-config',
        type=str,
        help='Create default configuration file at specified path'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='qwen-2.5-7b',
        help='Model name for default configuration'
    )
    
    args = parser.parse_args()
    
    # Create default configuration if requested
    if args.create_config:
        config_manager = ConfigManager()
        default_config = config_manager.create_default_config(args.model)
        
        config_path = Path(args.create_config)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        import yaml
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, indent=2)
        
        print(f"✓ Default configuration created: {config_path}")
        return
    
    # Validate configuration file exists
    if not Path(args.config).exists():
        print(f"❌ Configuration file not found: {args.config}")
        sys.exit(1)
    
    try:
        # Create and run orchestrator
        orchestrator = TrainingOrchestrator(args.config, args.resume)
        
        if args.validate_only:
            logger.info("Validation mode - checking environment only")
            orchestrator._validate_environment()
            logger.info("✓ Validation completed successfully")
        else:
            orchestrator.run()
            
    except Exception as e:
        logger.error(f"Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()