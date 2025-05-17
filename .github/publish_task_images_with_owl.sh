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
# echo "Building and publishing task base image..."
# image_name="$GITHUB_REGISTRY/$GITHUB_USERNAME/task-base-image"
# docker build -t "$image_name:$VERSION" -t "$image_name:latest" "workspaces/base_image"
# docker push "$image_name:$VERSION"
# docker push "$image_name:latest"
echo "Pulling task base image..."
image_name="$GITHUB_REGISTRY/$GITHUB_USERNAME/task-base-image"
docker pull "$image_name:$VERSION"

# Build and publish each task image
for task_dir in workspaces/tasks/*/; do
    task_name=$(basename "$task_dir")

    # skip task "ml-generate-gradcam" which is too large to build on GitHub Actions
    # it's okay to skip because evaluation script would then build OWL dependencies on the fly
    if [ "$task_name" == "ml-generate-gradcam" ]; then
        continue
    fi

    image_name="$GITHUB_REGISTRY/$GITHUB_USERNAME/$task_name-owl-image"
    
    echo "Building $task_name..."
    docker build -t "$image_name:$VERSION" -t "$image_name:latest" "$task_dir"
    
    echo "Publishing $task_name..."
    docker push "$image_name:$VERSION"
    docker push "$image_name:latest"

    docker image rm $image_name 
done

echo "All owl images have been built and published successfully!"