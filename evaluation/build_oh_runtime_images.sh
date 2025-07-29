#!/bin/bash
set -e

# RUN_NPC_TASKS_ONLY is a flag to build runtime images only for tasks that have scenarios.json defined
# When true, tasks without scenarios.json will be skipped
RUN_NPC_TASKS_ONLY=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --run-npc-tasks-only)
            RUN_NPC_TASKS_ONLY=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 [--run-npc-tasks-only]"
            exit 1
            ;;
    esac
done

echo "Run NPC tasks only: $RUN_NPC_TASKS_ONLY"

# Build and cache each OpenHands runtime image
for task_dir in workspaces/tasks/*/; do
    task_name=$(basename "$task_dir")
    
    # Check if run-npc-tasks-only mode is enabled and task doesn't have scenarios.json
    if [ "$RUN_NPC_TASKS_ONLY" = true ] && [ ! -f "$task_dir/scenarios.json" ]; then
        echo "Skipping $task_name - no scenarios.json found (run-npc-tasks-only mode enabled)"
        continue
    fi
    
    task_image_name="ghcr.io/theagentcompany/$task_name-image:1.0.0"

    echo "Pulling task image $task_image_name..."
    docker pull $task_image_name

    echo "Building OpenHands runtime image..."
    poetry run python evaluation/run_eval.py \
        --task-image-name "$task_image_name" \
        --build-image-only True
done

echo "All OpenHands runtime images have been built and cached locally!"