"""
TAC-RL: TheAgentCompany Reinforcement Learning Training System
==============================================================

A comprehensive system for training open-source language models using 
reinforcement learning on TheAgentCompany's professional task benchmark.

Author: Claude (Anthropic)
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Claude (Anthropic)"
__email__ = "noreply@anthropic.com"
__description__ = "Reinforcement Learning training system for TheAgentCompany benchmark"

from .architecture import (
    TACRLArchitecture,
    TrainingConfig,
    ModelConfig,
    TaskConfig,
    TrainingResult,
    TaskDomain,
    TrainingPhase
)

from .config_manager import ConfigManager

# Make key classes available at package level
__all__ = [
    'TACRLArchitecture',
    'TrainingConfig', 
    'ModelConfig',
    'TaskConfig',
    'TrainingResult',
    'TaskDomain',
    'TrainingPhase',
    'ConfigManager'
]