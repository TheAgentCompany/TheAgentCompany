"""
Local OpenHands Integration for TAC-RL
======================================

Updated OpenHands runner that uses the SAME local model for both
task execution and training - ensuring the agent actually improves!
"""

import asyncio
import os
import tempfile
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import docker
from datetime import datetime, timedelta

# OpenHands imports
from openhands.controller.state.state import State
from openhands.core.config import (
    OpenHandsConfig,
    SandboxConfig,
    LLMConfig,
)
from openhands.core.config.agent_config import AgentConfig
from openhands.core.config.condenser_config import NoOpCondenserConfig
from openhands.core.main import create_runtime, run_controller
from openhands.events.action import CmdRunAction, MessageAction
from openhands.events.observation import CmdOutputObservation
from openhands.runtime.base import Runtime
from openhands.utils.async_utils import call_async_from_sync

from ..architecture import TaskConfig, TrainingResult, TrainingConfig

class LocalOpenHandsRunner:
    """OpenHands runner using local trained model"""
    
    def __init__(self, config: TrainingConfig, art_trainer=None):
        self.config = config
        self.art_trainer = art_trainer  # Reference to the ART trainer with the model
        self.logger = logging.getLogger(__name__)
        
        # Docker client for container management
        self.docker_client = docker.from_env()
        
        # Runtime cache
        self.runtime_cache = {}
        self.task_timeouts = {}
        
        # Local model server setup
        self.local_model_server = None
        self._setup_local_model_server()
        
    def _setup_local_model_server(self):
        """Setup local model server for OpenHands"""
        
        # For now, we'll use the ART trainer's model directly
        # In production, you might want to run a separate vLLM server
        if self.art_trainer:
            self.logger.info("Using ART trainer's model for OpenHands execution")
        else:
            self.logger.warning("No ART trainer provided - will use external API as fallback")
    
    async def execute_task(self, task: TaskConfig) -> TrainingResult:
        """Execute a single task using the local trained model"""
        
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Starting local execution of task: {task.name}")
            
            # Create temporary directory for this task
            with tempfile.TemporaryDirectory() as temp_dir:
                
                # Setup OpenHands configuration with local model
                oh_config = self._create_openhands_config(task, temp_dir)
                
                # Get or create runtime
                runtime = self._get_runtime(task, oh_config)
                
                # Initialize task environment
                self._initialize_task_environment(runtime, task)
                
                # Execute the task using our trained model
                state = await self._run_task_with_local_model(runtime, task, oh_config)
                
                # Collect results
                result = self._process_results(task, state, temp_dir, start_time)
                
                self.logger.info(
                    f"Task {task.name} completed: "
                    f"success={result.success}, reward={result.reward:.3f}"
                )
                
                return result
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Task {task.name} failed with error: {e}", exc_info=True)
            
            return TrainingResult(
                task_name=task.name,
                success=False,
                reward=0.0,
                steps_taken=0,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _create_openhands_config(self, task: TaskConfig, temp_dir: str) -> OpenHandsConfig:
        """Create OpenHands configuration for local model execution"""
        
        # Determine task image name
        task_image = f"ghcr.io/theagentcompany/{task.name}-image:1.0.0"
        
        # Create LLM config for LOCAL model
        if self.art_trainer and hasattr(self.art_trainer, 'model'):
            # Use the trained model directly
            llm_config = LLMConfig(
                model="local-trained-model",  # Custom identifier
                base_url="http://localhost:8000/v1",  # Local server (if running)
                api_key="EMPTY"  # No external API needed
            )
        else:
            # Fallback to external API (for initial training)
            llm_config = LLMConfig(
                model=self.config.model.base_model_path,
                api_key=os.environ.get('OPENAI_API_KEY'),
                base_url=os.environ.get('LLM_BASE_URL'),
            )
        
        # Create OpenHands config
        config = OpenHandsConfig(
            run_as_openhands=False,
            max_budget_per_task=4.0,
            max_iterations=task.max_steps,
            save_trajectory_path=os.path.join(temp_dir, f'traj_{task.name}.json'),
            sandbox=SandboxConfig(
                base_container_image=task_image,
                enable_auto_lint=True,
                use_host_network=True,
                timeout=task.timeout_minutes * 60,
                api_key=os.environ.get('ALLHANDS_API_KEY', None),
            ),
            workspace_mount_path=temp_dir,
            workspace_mount_path_in_sandbox='/outputs',
        )
        
        config.set_llm_config(llm_config)
        
        # Configure agent
        agent_config = AgentConfig(
            enable_prompt_extensions=False,
            enable_history_truncation=False,
            enable_som_visual_browsing=False,
            condenser=NoOpCondenserConfig(),
        )
        config.set_agent_config(agent_config)
        
        return config
    
    def _get_runtime(self, task: TaskConfig, config: OpenHandsConfig) -> Runtime:
        """Get or create runtime for task execution"""
        
        # Use task image as cache key
        cache_key = config.sandbox.base_container_image
        
        if cache_key not in self.runtime_cache:
            self.logger.info(f"Creating new runtime for {task.name}")
            
            try:
                runtime = create_runtime(config)
                call_async_from_sync(runtime.connect)
                self.runtime_cache[cache_key] = runtime
                
            except Exception as e:
                self.logger.error(f"Failed to create runtime for {task.name}: {e}")
                raise
        
        return self.runtime_cache[cache_key]
    
    def _initialize_task_environment(self, runtime: Runtime, task: TaskConfig):
        """Initialize the task environment within the container"""
        
        # Load task dependencies
        dependencies = self._load_task_dependencies(runtime, task)
        
        # Initialize environment
        init_command = self._build_init_command(task, dependencies)
        
        self.logger.debug(f"Initializing environment for {task.name}")
        
        action = CmdRunAction(command=init_command)
        action.set_hard_timeout(900)  # 15 minutes for initialization
        
        obs = runtime.run_action(action)
        
        if obs.exit_code != 0:
            self.logger.error(f"Environment initialization failed for {task.name}: {obs.content}")
            raise RuntimeError(f"Failed to initialize task environment: {obs.content}")
            
        self.logger.debug(f"Environment initialized successfully for {task.name}")
    
    def _load_task_dependencies(self, runtime: Runtime, task: TaskConfig) -> List[str]:
        """Load service dependencies for the task"""
        
        command = "cat /utils/dependencies.yml"
        action = CmdRunAction(command=command)
        
        obs: CmdOutputObservation = runtime.run_action(action)
        
        if obs.exit_code != 0:
            self.logger.warning(f"Could not load dependencies for {task.name}")
            return []
        
        try:
            import yaml
            dependencies = yaml.safe_load(obs.content) or []
            self.logger.debug(f"Task {task.name} dependencies: {dependencies}")
            return dependencies
        except Exception as e:
            self.logger.warning(f"Failed to parse dependencies for {task.name}: {e}")
            return []
    
    def _build_init_command(self, task: TaskConfig, dependencies: List[str]) -> str:
        """Build the initialization command for the task environment"""
        
        # Base environment variables
        env_vars = [
            f"SERVER_HOSTNAME={os.environ.get('SERVER_HOSTNAME', 'localhost')}",
            f"LITELLM_API_KEY={os.environ.get('OPENAI_API_KEY', '')}",
            f"LITELLM_BASE_URL={os.environ.get('LLM_BASE_URL', '')}",
            f"LITELLM_MODEL={self.config.model.base_model_path}",
        ]
        
        # Build command
        command_parts = env_vars + [
            'echo "" | sudo tee -a /etc/hosts &&',
            'bash /utils/init.sh'
        ]
        
        return ' '.join(command_parts)
    
    async def _run_task_with_local_model(
        self, 
        runtime: Runtime, 
        task: TaskConfig, 
        config: OpenHandsConfig
    ) -> State:
        """Run the task using the local trained model"""
        
        # Create instruction for the agent
        instruction = self._create_task_instruction(task)
        
        # Set timeout tracking
        timeout_seconds = task.timeout_minutes * 60
        self.task_timeouts[task.name] = datetime.now() + timedelta(seconds=timeout_seconds)
        
        try:
            # Create custom controller that uses our local model
            if self.art_trainer and hasattr(self.art_trainer, 'generate_completion'):
                # Use the trained model for generation
                state = await self._run_with_local_model_controller(
                    runtime, task, instruction, config
                )
            else:
                # Fallback to standard OpenHands controller
                state = await run_controller(
                    config=config,
                    sid=task.name,
                    initial_user_action=MessageAction(content=instruction),
                    runtime=runtime,
                    fake_user_response_fn=self._create_user_response_fn(task),
                )
            
            return state
            
        except asyncio.TimeoutError:
            self.logger.warning(f"Task {task.name} timed out after {task.timeout_minutes} minutes")
            raise
        
        finally:
            # Clean up timeout tracking
            if task.name in self.task_timeouts:
                del self.task_timeouts[task.name]
    
    async def _run_with_local_model_controller(
        self,
        runtime: Runtime,
        task: TaskConfig,
        instruction: str,
        config: OpenHandsConfig
    ) -> State:
        """Custom controller that uses the local trained model"""
        
        # This is a simplified version - in practice you'd integrate more deeply
        # with OpenHands' controller architecture
        
        messages = [{"role": "user", "content": instruction}]
        state = State()  # Initialize empty state
        
        max_iterations = config.max_iterations
        
        for iteration in range(max_iterations):
            try:
                # Get response from our trained model
                response = await self.art_trainer.generate_completion(messages)
                
                if not response:
                    break
                
                # Add to message history
                messages.append({"role": "assistant", "content": response})
                
                # Parse and execute any commands in the response
                # This is a simplified version - real implementation would parse
                # OpenHands action format and execute them properly
                
                if "exit" in response.lower() or "finished" in response.lower():
                    break
                    
                # For now, just add the interaction to state
                state.history.append({
                    "action": "message",
                    "source": "assistant", 
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                
                if iteration >= max_iterations - 1:
                    self.logger.warning(f"Task {task.name} reached max iterations")
                    break
                    
            except Exception as e:
                self.logger.error(f"Error in local model execution: {e}")
                break
        
        return state
    
    def _create_task_instruction(self, task: TaskConfig) -> str:
        """Create the initial instruction for the task"""
        
        instruction = f"""You are an AI assistant helping with professional tasks. 

Your current task is: {task.name}

Please read the detailed task instructions in /instruction/task.md and complete the task step by step.

Available services and credentials:"""
        
        # Add service-specific credentials if needed
        if 'gitlab' in task.services_required:
            instruction += "\n- GitLab: http://localhost:8080 (username: root, password: theagentcompany)"
        
        if 'plane' in task.services_required:
            instruction += "\n- Plane: http://localhost:3001"
            
        if 'rocketchat' in task.services_required:
            instruction += "\n- RocketChat: http://localhost:3000"
            
        if 'owncloud' in task.services_required:
            instruction += "\n- ownCloud: http://localhost:8081"
        
        instruction += """\n\nPlease work through the task systematically and let me know when you're done or if you need help."""
        
        return instruction
    
    def _create_user_response_fn(self, task: TaskConfig):
        """Create user response function for agent interaction"""
        
        def user_response_fn(state: State) -> str:
            # Check if we're approaching timeout
            if task.name in self.task_timeouts:
                time_remaining = (self.task_timeouts[task.name] - datetime.now()).total_seconds()
                if time_remaining < 300:  # 5 minutes warning
                    return (
                        'You have less than 5 minutes remaining. Please focus on completing '
                        'the core task requirements. If you cannot complete the task, '
                        'please summarize what you have accomplished and finish.'
                    )
            
            # Standard response
            msg = (
                'Please continue working on the task. Focus on completing the requirements. '
                'If you think you have completed the task, please summarize what you did '
                'and finish the interaction.'
            )
            
            # Check interaction count for potential give-up
            if state.history:
                user_msgs = [
                    event for event in state.history
                    if isinstance(event, dict) and event.get('source') == 'user'
                ]
                if len(user_msgs) >= 3:
                    msg += '\nIf you want to give up, please explain what prevented completion and finish.'
            
            return msg
            
        return user_response_fn
    
    def _process_results(
        self, 
        task: TaskConfig, 
        state: State, 
        temp_dir: str, 
        start_time: datetime
    ) -> TrainingResult:
        """Process execution results and create TrainingResult"""
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Save trajectory
        trajectory_path = os.path.join(temp_dir, f'traj_{task.name}.json')
        
        # Run evaluation
        evaluation_result = self._run_task_evaluation(task, trajectory_path, temp_dir)
        
        # Extract metrics
        success = evaluation_result.get('success', False)
        reward = float(evaluation_result.get('reward', 0.0))
        checkpoints_passed = evaluation_result.get('checkpoints_passed', 0)
        
        # Count steps from state
        steps_taken = len(state.history) if state and state.history else 0
        
        # Copy trajectory to permanent storage if configured
        permanent_trajectory_path = None
        if self.config.output_dir:
            output_dir = Path(self.config.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            permanent_trajectory_path = output_dir / f'traj_{task.name}_{datetime.now().isoformat()}.json'
            
            if os.path.exists(trajectory_path):
                import shutil
                shutil.copy2(trajectory_path, permanent_trajectory_path)
        
        return TrainingResult(
            task_name=task.name,
            success=success,
            reward=reward,
            steps_taken=steps_taken,
            execution_time=execution_time,
            trajectory_path=str(permanent_trajectory_path) if permanent_trajectory_path else None,
            checkpoints_passed=checkpoints_passed,
            total_checkpoints=task.checkpoint_count
        )
    
    def _run_task_evaluation(self, task: TaskConfig, trajectory_path: str, temp_dir: str) -> Dict[str, Any]:
        """Run the task evaluation using TheAgentCompany's evaluator"""
        
        try:
            # Get runtime for evaluation
            runtime = self.runtime_cache.get(f"ghcr.io/theagentcompany/{task.name}-image:1.0.0")
            if not runtime:
                self.logger.error(f"No runtime available for evaluating {task.name}")
                return {'success': False, 'reward': 0.0}
            
            # Build evaluation command
            eval_command = (
                f"LITELLM_API_KEY={os.environ.get('OPENAI_API_KEY', '')} "
                f"LITELLM_BASE_URL={os.environ.get('LLM_BASE_URL', '')} "
                f"LITELLM_MODEL={self.config.model.base_model_path} "
                f"DECRYPTION_KEY='theagentcompany is all you need' "
                f"python_default /utils/eval.py "
                f"--trajectory_path /outputs/traj_{task.name}.json "
                f"--result_path /outputs/eval_{task.name}.json"
            )
            
            # Run evaluation
            action = CmdRunAction(command=eval_command)
            action.set_hard_timeout(600)  # 10 minutes for evaluation
            
            obs = runtime.run_action(action)
            
            if obs.exit_code != 0:
                self.logger.error(f"Evaluation failed for {task.name}: {obs.content}")
                return {'success': False, 'reward': 0.0}
            
            # Load evaluation results
            eval_result_path = os.path.join(temp_dir, f'eval_{task.name}.json')
            
            if os.path.exists(eval_result_path):
                with open(eval_result_path, 'r') as f:
                    eval_data = json.load(f)
                    
                return {
                    'success': eval_data.get('success', False),
                    'reward': float(eval_data.get('score', 0.0)),
                    'checkpoints_passed': len([
                        cp for cp in eval_data.get('checkpoints', [])
                        if cp.get('passed', False)
                    ])
                }
            else:
                self.logger.warning(f"Evaluation result file not found for {task.name}")
                return {'success': False, 'reward': 0.0}
                
        except Exception as e:
            self.logger.error(f"Error during evaluation of {task.name}: {e}", exc_info=True)
            return {'success': False, 'reward': 0.0}
    
    def cleanup(self):
        """Clean up resources"""
        self.logger.info("Cleaning up LocalOpenHands runner resources")
        
        # Close cached runtimes
        for runtime in self.runtime_cache.values():
            try:
                if hasattr(runtime, 'close'):
                    runtime.close()
            except Exception as e:
                self.logger.warning(f"Error closing runtime: {e}")
        
        self.runtime_cache.clear()
        self.task_timeouts.clear()
        
        # Clean up local model server
        if self.local_model_server:
            try:
                # Stop local server if running
                pass
            except:
                pass