# Task Images Generator

This script generates Docker image URLs based on task names in the `workspaces/tasks` directory.

## Features

- Scans all subdirectories in the `workspaces/tasks` directory
- Generates image URLs based on the logic from `evaluation/run_eval.sh`
- Supports excluding tasks with `scenarios.json` files
- Supports excluding tasks with LLM function calls (`llm_complete`, `evaluate_with_llm`, `evaluate_chat_history_with_llm`)
- Supports excluding multiple types of tasks simultaneously
- Outputs formatted JSON files

## Image URL Format

Based on the logic from `run_eval.sh`, the image URL format is:
```
ghcr.io/theagentcompany/${task_name}-image:${VERSION}
```

Where:
- `task_name` is the subdirectory name in the `workspaces/tasks` directory
- `VERSION` defaults to "1.0.0"

## Usage

### Basic Usage
```bash
python generate_task_images.py
```

### Specify Output File
```bash
python generate_task_images.py --output task_images.json
```

### Exclude Tasks with scenarios.json
```bash
python generate_task_images.py --exclude-scenarios --output task_images_no_scenarios.json
```

### Exclude Tasks with LLM Function Calls
```bash
python generate_task_images.py --exclude-llm-functions --output task_images_no_llm.json
```

### Exclude Both scenarios.json and LLM Function Calls
```bash
python generate_task_images.py --exclude-scenarios --exclude-llm-functions --output task_images_clean.json
```

### Specify Version
```bash
python generate_task_images.py --version 2.0.0 --output task_images_v2.json
```

### Specify Tasks Directory
```bash
python generate_task_images.py --tasks-dir /path/to/tasks --output task_images.json
```

### Combined Usage
```bash
python generate_task_images.py --exclude-scenarios --exclude-llm-functions --version 2.0.0 --output task_images_v2_clean.json
```

## Parameters

- `--tasks-dir`: Path to the tasks directory (default: `../workspaces/tasks` relative to script location)
- `--version`: Image version tag (default: `1.0.0`)
- `--output`: Output JSON file path (optional, prints to stdout if not specified)
- `--exclude-scenarios`: Exclude tasks that have `scenarios.json` files
- `--exclude-llm-functions`: Exclude tasks that have LLM function calls (detects `llm_complete`, `evaluate_with_llm`, `evaluate_chat_history_with_llm`)

## Output Format

### Basic Output Format
```json
{
  "version": "1.0.0",
  "total_tasks": 175,
  "exclude_scenarios": false,
  "exclude_llm_functions": false,
  "tasks": [
    {
      "task_name": "admin-arrange-meeting-rooms",
      "image_url": "ghcr.io/theagentcompany/admin-arrange-meeting-rooms-image:1.0.0",
      "version": "1.0.0"
    },
    ...
  ]
}
```

### Output Format with Exclusion Parameters
```json
{
  "version": "1.0.0",
  "total_tasks": 105,
  "exclude_scenarios": true,
  "exclude_llm_functions": true,
  "excluded_tasks": [
    {
      "task_name": "admin-ask-for-meeting-feedback",
      "reasons": ["scenarios.json"]
    },
    {
      "task_name": "admin-ask-for-upgrade-reimbursement",
      "reasons": ["scenarios.json", "LLM functions"]
    },
    ...
  ],
  "excluded_count": 70,
  "excluded_scenarios_count": 41,
  "excluded_scenarios_tasks": [
    "admin-ask-for-meeting-feedback",
    ...
  ],
  "excluded_llm_count": 53,
  "excluded_llm_tasks": [
    "admin-ask-for-upgrade-reimbursement",
    ...
  ],
  "tasks": [
    {
      "task_name": "admin-arrange-meeting-rooms",
      "image_url": "ghcr.io/theagentcompany/admin-arrange-meeting-rooms-image:1.0.0",
      "version": "1.0.0"
    },
    ...
  ]
}
```

## Examples

### Generate Image URLs for All Tasks
```bash
python generate_task_images.py --output all_tasks.json
# Output: 175 task image URLs
```

### Exclude Tasks with scenarios.json
```bash
python generate_task_images.py --exclude-scenarios --output no_scenarios_tasks.json
# Output: 134 task image URLs, excluded 41 tasks with scenarios.json
```

### Exclude Tasks with LLM Function Calls
```bash
python generate_task_images.py --exclude-llm-functions --output no_llm_tasks.json
# Output: 122 task image URLs, excluded 53 tasks with LLM function calls
```

### Exclude Both scenarios.json and LLM Function Calls
```bash
python generate_task_images.py --exclude-scenarios --exclude-llm-functions --output clean_tasks.json
# Output: 105 task image URLs, excluded 70 tasks (41 scenarios.json + 53 LLM functions, with overlap)
```

The generated JSON files can be used for:
- Batch pulling Docker images
- Generating task lists
- Automated deployment scripts
- Other scenarios requiring task name and image URL mapping

## Detected LLM Functions

The script detects the following three LLM functions:
- `llm_complete`: Used for completing LLM conversations
- `evaluate_with_llm`: Used for evaluating content with LLM
- `evaluate_chat_history_with_llm`: Used for evaluating chat history with LLM 