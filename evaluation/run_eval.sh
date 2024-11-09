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
    poetry run python run_eval.py --llm-config claude --task_image_name "${task_name}-image"

    # Return to current directory
    cd -

    # Remove task image
    echo "Removing task image..."
    make stop
    
    # Return to tasks directory for next iteration
    cd ..
done

echo "All evaluation completed successfully!"