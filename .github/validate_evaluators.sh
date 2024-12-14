#!/bin/bash
set -e

task_type=$1
task_types=("pm" "sde")

for task_dir in workspaces/tasks/*/; do
  task_name=$(basename $task_dir)
  if [ "$task_type" != "other" ]; then
      if [[ "$task_name" != "$task_type"* ]]; then
          continue
      fi
  else
      # Extract the part of task_dir before the first "-"
      task_prefix="${task_name%%-*}"
      if [[ " ${task_types[@]} " =~ " ${task_prefix} " ]]; then
          continue
      fi
  fi
  
  echo "Testing in $task_dir"
  cd "$task_dir"

  docker build -t task-image .

  # Run the container and execute the evaluator
  # The evaluator would almost always say 0 marks granted, but that's
  # fine, we only run it to make sure it at least compiles
  docker run -e TAC_TEST_MODE=true --rm task-image sh -c \
    "echo '127.0.0.1 the-agent-company.com' >> /etc/hosts; \
    DECRYPTION_KEY='theagentcompany is all you need' python_default /utils/eval.py"

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
