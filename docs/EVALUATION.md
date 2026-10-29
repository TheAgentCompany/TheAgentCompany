# Evaluation Guidelines

Make sure you have all services launched and running before you start evaluation. If not,
please refer to the [SERVER SETUP DOC](./SETUP.md) first.

Since many tasks require LLMs to evaluate the results, and/or require
NPCs backed by LLMs to play the roles of coworkers, we require you to provide an LLM API key as
"environment LLM config". This LLM API key does not need to be the same as the one you use for your
agent(s). It needs to be as powerful as or at least close to `claude-3-5-sonnet-20241022` or `gpt-4o`.
For reference, all baseline results used `claude-3-5-sonnet-20241022` as the environment LLM. Please
provide the environment LLM model you use when you submit your results to the leaderboard.

To prevent the agent from peeking at the evaluator code, all `/utils/evaluator.py` files, which contain
the grading functions, are encrypted. The evaluator entrypoint, `/utils/eval.py`, contains the decryption
code, and you need to pass the decryption key as an environment variable when you run it: `DECRYPTION_KEY='theagentcompany is all you need'`.

The section below describes the general steps to run evaluation. Different platforms
or agents might require variation on steps, but the general principles should hold. If you'd like to use
[OpenHands](https://github.com/All-Hands-AI/OpenHands) for evaluation, please refer to the [RUN EVALUATION WITH OPENHANDS](../evaluation/README.md) doc.
You could also use it as a reference to automate your evaluation pipeline.

## General Steps

TheAgentCompany 1.0.0 evaluation consists of 175 tasks. Each task is a Docker image.
A complete list of tasks can be found [here](../workspaces/README.md).

### Step 1: Start Task Container

Start the container manually by running:

```bash
docker run --name <container_name> --network host -it <image_name> /bin/bash
```

Caveat: `--network host` is only needed if you are running servers and the task
container on the same machine, i.e. your `SERVER_HOSTNAME=localhost`. If you have
a public hostname (e.g. aws ec2 address) for servers, then this flag is not needed.
Note that this flag is only available on Linux. If you are using Macbook or Windows,
and your servers are running on `localhost`, you need to ensure `Settings > Resources > Network > Enable host networking` is enabled on your Docker Desktop.


### Step 2: Initialize the Task Environment

```bash
SERVER_HOSTNAME=<hostname, default value is localhost> \
LITELLM_API_KEY=<environment_llm_api_key> \
LITELLM_BASE_URL=<environment_llm_base_url> \
LITELLM_MODEL=<environment_llm_model_name> \
bash /utils/init.sh
```

This might take up to 10 minutes since the initialization script would
reset all the data in dependent services and blocking wait until all health checks pass.

Most importantly, the initialization script would add the server's IP to the `/etc/hosts` file,
so that the agent can visit the services using the synthetic `the-agent-company.com` hostname.

Your servers could be running locally (in which case `localhost` is used as SERVER_HOSTNAME),
or remotely (e.g. an AWS host like ec2-ip.us-east-2.compute.amazonaws.com)

### Step 3: Conduct the Task

Now you can prompt the agent to work on the task. The task instruction is at `/instruction/task.md`
in the task container. For reference, in the baseline evaluation, we prompt the agent with:

> Complete the task in /instruction/task.md

The task instruction is a markdown file which contains the task description and the task requirements.
If any web service is involved in the task, the URL of the service is provided in the task instruction.

Your agent doesn't have to do browsing in the container environment. The baseline agent
installs a headless chrome in the container for browsing purposes, but your agent doesn't
have to. It could, for example, use a normal browser on a computer just like what human
beings do. If you do choose this way, please bear in mind that some tasks involve uploading
and downloading steps, and you might want to use mounting to transfer files between the
task container and the host machine.

Caveat: all services require username and password. We allow benchmark users to use whatever
ways they want to provide the username and password. You could add username and password to
the prompt, or cache the login session cookie in the browser. For reference, in the
baseline evaluation, we use OpenHands platform to deterministically login to all services
before letting the agent work on the task. We still provide GitLab username and password
in the system prompt since running `git` commands sometimes requires the username and password.
You could refer to the [browsing.py](../evaluation/browsing.py)
file to see how we login to all services.

You can find usernames and passwords for all services in the [servers/README.md](../servers/README.md).

### Step 4: Evaluate the Result

Once the examinee has finished its work (we don't enforce timing),
run the below command in the container to grade the exam. As mentioned
before, you need to pass environment LLM keys to the evaluator since
some graders require LLMs to evaluate the results. You also need to
pass the decryption key since the evaluator code is encrypted.

For checkpoint predicates evaluated through Codex CLI, set `CODEX_JUDGE_MODEL` to the
explicit Codex model identifier and make Codex CLI available in a trusted evaluator
runtime, isolated from the examinee. Authenticate that runtime using `codex login --device-auth`
and keep its credential directory outside the examinee container and workspace. The evaluator
does not perform interactive authentication. It disables shell, apps, browser, computer,
subagent and code-mode tools and uses an ephemeral read-only session. Use `CODEX_CLI` to
select the executable and `CODEX_JUDGE_TIMEOUT_SECONDS` to adjust the per-judgment timeout
(default: 120 seconds). The mini deployment procedure uses a separate trusted grader container.
The existing `LITELLM_*` settings remain necessary for NPCs and any other LLM-based runtime
behavior. Codex judging uses the same yes/no predicate and does not change checkpoint weights
or scoring strategies.

```bash
LITELLM_API_KEY=<environment_llm_api_key> \
LITELLM_BASE_URL=<environment_llm_base_url> \
LITELLM_MODEL=<environment_llm_model_name> \
CODEX_JUDGE_MODEL=<codex_model_id> \
DECRYPTION_KEY='theagentcompany is all you need' \
python_default /utils/eval.py --trajectory_path TRAJECTORY_PATH --result_path RESULT_PATH
```

whose usage is:

```
usage: eval.py [-h] [--trajectory_path TRAJECTORY_PATH] [--result_path RESULT_PATH]

Grade checkpoints from trajectory and save results

options:
  -h, --help            show this help message and exit
  --trajectory_path TRAJECTORY_PATH
                        Path to the trajectory file
  --result_path RESULT_PATH
                        Path to save the output JSON
```

Note that trajectory file is optional. It is often used to grant partial credits.
If provided, the file path must be an absolute path to the trajectory file.
There is no specific requirement on the trajectory file's content and format,
but it MUST record all steps conducted by the examinee (no matter it's agent or
human being). Benchmark users are allowed to inspect checkpoint rubrics to ensure
the trajectory contains all necessary information used in graders, but examinees
(e.g. agents) are not allowed to read checkpoint rubrics or evaluation code.
