# TAC-RL: TheAgentCompany Reinforcement Learning Training System

A comprehensive system for training open-source language models using reinforcement learning on TheAgentCompany's real-world professional task benchmark.

## 🏗️ Architecture Overview

```
TAC-RL Pipeline:
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   TheAgentCompany   │────▶│     OpenHands       │────▶│   OpenPipe ART      │
│   (Environment)     │    │   (Agent Runtime)   │    │  (RL Training)      │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
         │                           │                           │
         ▼                           ▼                           ▼
    Task Sampling              Agent Execution            GRPO Optimization
    Reward Computation         Trajectory Collection      Model Updates
    Evaluation                 Multi-Service Integration   Checkpointing
```

## 🎯 Key Features

- **Multi-Domain Training**: 175+ professional tasks across 8 domains
- **Efficient RL**: GRPO algorithm with minimal compute requirements
- **Real-World Complexity**: Multi-service environments (GitLab, Plane, RocketChat)
- **Scalable Architecture**: Modular design for easy extension
- **Comprehensive Monitoring**: Detailed logging and progress tracking

## 🚀 Quick Start

```bash
# 1. Setup environment
./setup.sh

# 2. Start training
python train.py --config configs/qwen_2_5_7b.yaml

# 3. Monitor progress
python monitor.py --run-id latest
```

## 📊 Expected Results

- **Performance**: 20-40% improvement on TAC benchmark
- **Cost**: ~$50-100 for full 7B model training
- **Time**: 2-5 days depending on hardware