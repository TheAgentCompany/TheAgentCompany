#!/bin/bash
set -e

# Build and publish each OpenHands runtime image
for task_dir in workspaces/tasks/*/; do
    task_name=$(basename "$task_dir")
    task_image_name="ghcr.io/TheAgentCompany/$task_name-image:$TAC_version"

    echo "Pulling task image $task_image_name..."
    docker pull $task_image_name

    echo "Building OpenHands runtime image..."
    poetry run python evaluation/run_eval.py \
        --task-image-name "$task_image_name" \
        --build-image-only True
done

echo "All OpenHands runtime images have been built and cached locally!"