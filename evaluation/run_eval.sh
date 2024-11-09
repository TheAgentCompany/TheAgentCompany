#!/bin/bash

# Exit on any error
set -e

# Check if current directory is "evaluation"
current_dir=$(basename "$PWD")
if [ "$current_dir" != "evaluation" ]; then
    echo "Error: Script must be run from the 'evaluation' directory"
    echo "Current directory is: $current_dir"
    exit 1
fi


# Set default values
# LLM_CONFIG is an OpenHands LLM config defined in config.toml
LLM_CONFIG="claude"
# OUTPUTS_PATH is the path to save trajectories and evaluation results
OUTPUTS_PATH="outputs"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --llm-config)
            LLM_CONFIG="$2"
            shift 2
            ;;
        --outputs_path)
            OUTPUTS_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

echo "Using LLM config: $llm_config"
echo "Outputs path: $outputs_path"

# Navigate to base image directory and build
echo "Building base image..."
cd ../workspaces/base_image
make build

# Navigate to tasks directory
cd ../tasks

# Iterate through each directory in tasks
for task_dir in */; do
    # Remove trailing slash from directory name
    task_name=${task_dir%/}

    # Check if evaluation file exists
    if [ -f "$outputs_path/eval_${task_name}-image.json" ]; then
        echo "Skipping $task_name - evaluation file already exists"
        continue
    fi
    
    echo "Running evaluation for task: $task_name"
    
    # Enter task directory
    cd "$task_dir"
    
    # Build task
    echo "Building $task_name..."
    make build
    
    # Navigate to evaluation folder and run evaluation
    echo "Running evaluation for $task_name..."
    cd ../../../evaluation
    # TODO: use CLI arg to specify llm_config
    poetry run python run_eval.py --llm-config $LLM_CONFIG --outputs_path $OUTPUTS_PATH --task_image_name "${task_name}-image"

    echo "Removing task image..."
    docker rm "${task_name}-image"
    
    # Return to tasks directory for next iteration
    cd ../tasks
done

echo "All evaluation completed successfully!"