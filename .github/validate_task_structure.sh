#!/bin/bash
set -e

cd workspaces/tasks

for task_dir in *; do
  # Check if folder name is lowercase
  if [ "$task_dir" != "$(echo $task_dir | tr '[:upper:]' '[:lower:]')" ]; then
    echo "Error: Folder name '$task_dir' is not in lowercase"
    exit 1
  fi

  echo "Checking task: $task_dir"
  cd "$task_dir"
  
  # 1. Check if task.md exists
  if [ ! -f "task.md" ]; then
    echo "Error: task.md is missing in $task_dir"
    exit 1
  fi

  # 2. Check evaluator.py
  if [ ! -f "evaluator.py" ]; then
    echo "Error: evaluator.py is missing in $task_dir"
    exit 1
  fi
  # Check for at least one @grader annotator
  if ! grep -q "@grader" evaluator.py; then
      echo "Error: evaluator.py must contain at least one @grader annotator, see example task for reference"
      exit 1
  fi

  # 3. Check Dockerfile
  if [ ! -f "Dockerfile" ]; then
    echo "Error: Dockerfile is missing in $task_dir"
    exit 1
  fi
  if ! grep -q "FROM ghcr.io/theagentcompany/task-base-image:1.0.0" "Dockerfile"; then
    echo "Error: Dockerfile in $task_dir does not contain 'FROM ghcr.io/theagentcompany/task-base-image:1.0.0'"
    exit 1
  fi
  # we don't allow CMD or ENTRYPOINT in task Dockerfiles, because OpenHands, or any other
  # agent might need to build their custom images on top of the task image, and override
  # the default CMD or ENTRYPOINT
  if grep -q "^[[:space:]]*CMD" "Dockerfile"; then
    echo "Error: Dockerfile in $task_dir contains CMD instruction which is not allowed"
    exit 1
  fi
  if grep -q "^[[:space:]]*ENTRYPOINT" "Dockerfile"; then
    echo "Error: Dockerfile in $task_dir contains ENTRYPOINT instruction which is not allowed"
    exit 1
  fi

  # 4. Check Makefile structure
  if [ ! -f "Makefile" ]; then
    echo "Error: Makefile is missing in $task_dir"
    exit 1
  fi
  if ! grep -q "build" "Makefile"; then
    echo "Error: Makefile in $task_dir does not contain 'build'"
    exit 1
  fi

  folder_name=$(basename "$task_dir")

  image_name=$(grep '^IMAGE_NAME=' Makefile | cut -d'=' -f2)
  expected_image_name="${folder_name}-image"
  if [ "$image_name" != "$expected_image_name" ]; then
    echo "Error: IMAGE_NAME in ${task_dir}/Makefile should be $expected_image_name"
    exit 1
  fi
  
  container_name=$(grep '^CONTAINER_NAME=' Makefile | cut -d'=' -f2)
  expected_container_name="${folder_name}"
  if [ "$container_name" != "$expected_container_name" ]; then
    echo "Error: CONTAINER_NAME in ${task_dir}/Makefile should be $expected_container_name"
    exit 1
  fi

  # 5. Check if checkpoints.md exists
  if [ ! -f "checkpoints.md" ]; then
    echo "Error: checkpoints.md is missing in $task_dir"
    exit 1
  fi

  # 6. Check dependencies.yml
  if [ ! -f "dependencies.yml" ]; then
    echo "Error: dependencies.yml is missing in $task_dir"
    exit 1
  fi

  poetry run python ../../../.github/validate_dependencies.py "dependencies.yml"

  cd -
done

echo "All checks passed successfully!"