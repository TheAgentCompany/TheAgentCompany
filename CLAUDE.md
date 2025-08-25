# CLAUDE.md - TheAgentCompany Repository Understanding

## Repository Overview
**TheAgentCompany** is a comprehensive benchmark for evaluating LLM agents on real-world professional tasks. It provides an extensible framework for testing AI agents' performance on consequential work-related tasks across multiple professional domains.

## Key Information
- **Language**: Python (3.12+)
- **License**: MIT
- **Main Framework**: OpenHands (0.42.0)
- **Architecture**: Multi-service containerized environment
- **Total Tasks**: 175 evaluation tasks
- **Paper**: https://arxiv.org/abs/2412.14161
- **Website**: https://the-agent-company.com/

## Project Structure

### Core Directories
```
/
├── docs/                          # Documentation and setup guides
├── evaluation/                    # Evaluation harness and scripts
├── servers/                       # Service containers (GitLab, Plane, etc.)
├── workspaces/                    # Task definitions and base images
│   ├── base_image/               # Common utilities and evaluation framework
│   └── tasks/                    # 175+ individual task definitions
└── pyproject.toml                # Python project configuration
```

### Key Files
- `README.md`: Main project documentation
- `evaluation/run_eval.py`: Primary evaluation runner
- `workspaces/base_image/eval.py`: Task evaluation entrypoint
- `servers/setup.sh`: Infrastructure setup script

## Professional Domains Covered
1. **Software Engineer** (swe-*)
2. **Product Manager** (pm-*)
3. **Data Scientist** (ds-*)
4. **Human Resources** (hr-*)
5. **Finance** (finance-*)
6. **Administration** (admin-*)
7. **Business/Marketing** (bm-*)
8. **Machine Learning** (ml-*)

## Infrastructure Services
- **GitLab**: Code repository and issue tracking
- **Plane**: Project management platform  
- **ownCloud**: File sharing and collaboration
- **RocketChat**: Team communication platform
- **API Server**: Central coordination service (port 2999)

## Task Architecture
Each task follows a standardized Docker container structure:
```
/utils/
├── evaluator.py.enc          # Encrypted evaluation logic
├── init.sh                   # Environment initialization
├── config.py                 # Task configuration
├── common.py                 # Shared utilities
├── eval.py                   # Evaluation entrypoint
└── dependencies.yml          # Service dependencies

/instruction/
└── task.md                   # Human-readable task description

/workspace/
└── [task-specific files]     # Working directory
```

## Evaluation Framework
- **Result-based evaluation**: Primary scoring method
- **Subcheckpoint evaluation**: Secondary validation
- **LLM-based evaluators**: For complex assessments
- **Deterministic evaluators**: For precise validation
- **Trajectory analysis**: Action sequence examination

## Key Components

### Evaluation System (`evaluation/run_eval.py`)
- OpenHands integration for agent execution
- Service dependency management  
- Pre-login automation for web services
- Trajectory recording and analysis
- Automated scoring and result generation

### Base Image (`workspaces/base_image/`)
- `eval.py`: Decrypts and executes task evaluators
- `common.py`: Shared utilities across tasks
- `scoring.py`: Result formatting and validation
- `npc/`: Non-player character (colleague simulation)

### Task Structure
Each task includes:
- `Dockerfile`: Container definition
- `Makefile`: Build automation
- `task.md`: Task instructions
- `evaluator.py`: Scoring logic (encrypted)
- `dependencies.yml`: Required services
- `checkpoints.md`: Validation criteria

## Setup Requirements
- Docker + Docker Compose
- 30+ GB free disk space
- Host networking enabled
- Python 3.12+

## Usage Patterns

### Quick Start
```bash
# Setup infrastructure
curl -fsSL setup_script_url | sh

# Run evaluation
cd evaluation
bash run_eval.sh --agent-llm-config <config> --outputs-path <path>
```

### Manual Task Execution
```bash
# Start task container
docker run --network host -it <task_image> /bin/bash

# Initialize environment  
SERVER_HOSTNAME=localhost bash /utils/init.sh

# Execute task
# (Agent works on /instruction/task.md)

# Evaluate results
python /utils/eval.py --trajectory_path <path>
```

## Security Note
- Evaluator logic is encrypted with key: "theagentcompany is all you need"
- Task containers run with host network access
- Service credentials are pre-configured (e.g., GitLab root:theagentcompany)

## Development Workflow
1. Service containers provide realistic work environment
2. Agents interact via web browsers, APIs, and file systems
3. Tasks require multi-step reasoning and tool usage
4. Evaluation captures both final results and process quality
5. Extensible framework allows adding new tasks and domains

## Notable Features
- **Multi-agent interaction**: NPCs simulate colleagues
- **Diverse data types**: Code, documents, images, databases
- **Real-world complexity**: Authentic professional scenarios  
- **Comprehensive scoring**: Multiple evaluation methodologies
- **Extensible design**: Easy addition of new tasks/evaluators

This repository represents a significant advancement in evaluating AI agents' capabilities for professional work, providing a robust testbed for measuring progress toward autonomous digital workers.