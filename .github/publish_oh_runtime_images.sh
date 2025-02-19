#!/bin/bash
set -e

# Check if version is provided
if [ -z "$1" ]; then
    echo "Error: Version parameter is required"
    echo "Usage: $0 <version>"
    exit 1
fi

# Validate version format (x.y.zOHa.b.c) and extract a.b.c
if [[ "$1" =~ ^([0-9]+\.[0-9]+\.[0-9]+)OH([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
    openhands_version="${BASH_REMATCH[2]}"
    echo "OpenHands version: $openhands_version"
    TAC_version="${BASH_REMATCH[1]}"
    echo "TheAgentCompany task version: $TAC_version"
else
    echo "Error: Version must be in format x.y.zOHa.b.c"
    echo "Example: 1.0.0OH0.14.2, representing TheAgentCompany version 1.0.0 tasks + OpenHands 0.14.2 runtime"
    exit 1
fi

VERSION=$1
GITHUB_REGISTRY="ghcr.io"
GITHUB_USERNAME=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f1 | tr '[:upper:]' '[:lower:]')
GITHUB_REPO=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f2)

# Login to GitHub Container Registry
# echo "$GITHUB_TOKEN" | docker login $GITHUB_REGISTRY -u $GITHUB_USERNAME --password-stdin

# Build and publish each OpenHands runtime image
for task_dir in workspaces/tasks/*/; do
    task_name=$(basename "$task_dir")
    task_image_name="$GITHUB_REGISTRY/$GITHUB_USERNAME/$task_name-image:$TAC_version"

    echo "Pulling task image $task_image_name..."
    docker pull $task_image_name

    echo "Building OpenHands runtime image..."
    poetry run python evaluation/run_eval.py \
        --task-image-name "$task_image_name" \
        --build-image-only True
    
    # echo "Building $task_name..."
    # docker build -t "$image_name:$VERSION" -t "$image_name:latest" "$task_dir"
    
    # echo "Publishing $task_name..."
    # docker push "$image_name:$VERSION"
    # docker push "$image_name:latest"
done

echo "All OpenHands runtime images have been built and published successfully!"