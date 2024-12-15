#!/bin/bash
set -e

# Check if version is provided
if [ -z "$1" ]; then
    echo "Error: Version parameter is required"
    echo "Usage: $0 <version>"
    exit 1
fi

VERSION=$1
GITHUB_REGISTRY="ghcr.io"
GITHUB_USERNAME=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f1 | tr '[:upper:]' '[:lower:]')
GITHUB_REPO=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f2)

# Login to GitHub Container Registry
echo "$GITHUB_TOKEN" | docker login $GITHUB_REGISTRY -u $GITHUB_USERNAME --password-stdin

# Publish task base image
echo "Building and publishing task base image..."
image_name="$GITHUB_REGISTRY/$GITHUB_USERNAME/task-base-image"
docker build -t "$image_name:$VERSION" -t "$image_name:latest" "workspaces/base_image"
docker push "$image_name:$VERSION"
docker push "$image_name:latest"

# Build and publish each task image
for task_dir in workspaces/tasks/*/; do
    task_name=$(basename "$task_dir")
    image_name="$GITHUB_REGISTRY/$GITHUB_USERNAME/$task_name-image"
    
    echo "Building $task_name..."
    docker build -t "$image_name:$VERSION" -t "$image_name:latest" "$task_dir"
    
    echo "Publishing $task_name..."
    docker push "$image_name:$VERSION"
    docker push "$image_name:latest"
done

echo "All images have been built and published successfully!"