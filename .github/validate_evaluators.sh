#!/bin/bash
set -e

for task_dir in workspaces/tasks/*/; do
  echo "Testing in $task_dir"
  cd "$task_dir"

  docker build -t task-image .

  # Run the container and execute the evaluator
  # The evaluator would almost always say 0 marks granted, but that's
  # fine, we only run it to make sure it at least compiles
  docker run -e TAC_TEST_MODE=true --rm task-image python_default /utils/eval.py

  # Capture the exit code
  EXIT_CODE=$?

  # If the evaluator failed, exit the workflow
  if [ $EXIT_CODE -ne 0 ]; then
    echo "Evaluator failed in $task_dir"
    exit $EXIT_CODE
  fi

  cd -
done

echo "Sanity check passed for all evaluators"
