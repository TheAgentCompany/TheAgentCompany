# Run Evaluation with OpenHands

This directory contains the baseline for The Agent Company. The baseline is conducted using
[OpenHands](https://github.com/All-Hands-AI/OpenHands), an open-source platform for software development agents powered by AI.

## Prerequisites

If you need to use OpenHands for evaluation, you also need:
1. python 3.12 or above
2. poetry
3. install dependencies using `poetry install` under project root directory
4. docker buildx

## Configuration

Please create a `config.toml` file under `evaluation` directory. It should look like this:

```toml
[llm.group1]
model="<model_name>"
base_url="<base_url>"
api_key="<api_key>"

[llm.group2]
model="<model_name>"
base_url="<base_url>"
api_key="<api_key>"
```

you can add more groups as needed.

## Run Evaluation

Under `evaluation` directory, run the following command:

```bash
bash run_eval.sh \
  --agent-llm-config group1 \
  --env-llm-config group2 \
  --outputs-path outputs \
  --server-hostname localhost \
  --version 1.0.0
```

where `--outputs-path`, `--server-hostname`, and `--version` are optional.

Here's a brief explanation of each argument:

- `--agent-llm-config`: the config name for the agent LLM. This should match the config name in `config.toml`. This is the LLM used by the agent (i.e. CodeActAgent).
- `--env-llm-config`: the config name for the environment LLM. This should match the config name in `config.toml`. This is used by the chat bots (NPCs) and LLM-based evaluators.
- `--outputs-path`: the path to save trajectories and evaluation results.
- `--server-hostname`: the hostname of the server that hosts all the web services. It could be `localhost` if you are running the evaluation and services on the same machine. If the services are hosted on a remote machine, you must use the hostname of the remote machine rather than IP address.
- `--version`: the version of the task images to use. Currently, the only supported version is `1.0.0`.

The script is idempotent. If you run it again, it will resume from the last checkpoint.
It would usually take a few days to finish evaluation.

Note: the script will automatically skip a task if it encounters an error. This usually
happens when the OpenHands runtime dies due to some unexpected errors. This means even
if the script finishes, it might not have evaluated all tasks. You can manually resume
the evaluation by running the script again.

## Analysis

You can find the evaluation results in the `outputs` directory, including trajectories,
evaluation scores, final agent states, and screenshots for all browsing steps.

You can run the following command to generate a summary of the evaluation results:

```bash
poetry run python summarise_results.py <outputs_path>
```

An example of the summary report can be found [here](https://github.com/TheAgentCompany/experiments/tree/main/evaluation/1.0.0/20241217_OpenHands-0.14.2-sonnet-20241022).
