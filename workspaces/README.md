## Workspace directory

This directory hosts workspaces that are local to the examinee (e.g. agents or actual human users).

Each task will have its own container image and related evaluation code, e.g. LLM-based evaluation or end-to-end tests.

## Benchmarking Guidelines

Make sure you have all services launched and running before you start evaluation.
This guideline uses [OpenHands](https://github.com/All-Hands-AI/OpenHands) and
[Example](./tasks/example) task. The exact steps might differ among various agents and actual human beings,
but the general principles should hold.

### Step 0: Launch All Services

Please refer to `servers` directory for instructions.

### Step 1: Build Base Image

This step only needs to be done once across all tasks. It builds a base image
that can be used by all exam (task) images.

```bash
# assume we are under workspaces directory
docker build -t base-image .
```

### Step 2: Build Exam Image

An exam image is the image used for a specific task. It can be built via:

```bash
# assume we are under workspaces directory
docker build -t example-exam-image tasks/example
```

An examinee should finish all its work in a container created out of this image.
The built container is analagous to a laptop used in an interview or daily work.

As a benchmark user (e.g. you'd like to evaluate an agent), you could run

```bash
python /evaluation/test_setup.py
```

in the exam container to testify the environment,
including but not limited to the connections between the task container and the
services hosted in separate containers or remotely.

### Step 3: Launch Agent

This step varies among examinees. We use OpenHands, a platform for software development
agents powered by AI.

OpenHands requires a sandbox environment that the agent needs to run in. It allows
users to provide a custom sandbox image, and thus we will use the `example-exam-image`
we just built.

Clone `OpenHands` repo and create a `config.toml` in the OpenHands directory:

```toml
[core]
workspace_base="/workspace"
run_as_openhands=true
sandbox_base_container_image="example-exam-image"
```

Please note you also need to add LLM keys to `config.toml`. Please follow OpenHands
documentation to complete the setup.

Then you can launch the agent and prompt it with the task. At the moment, with
OpenHands, you need to do it manually. You could prompt the agent with, say,

> Complete the task in /instruction/task.md

### Step 4: Run Evaluation

Once the examinee has finished its work (as of now, we don't enforce timing),
run the below command in the exam container to grade the exam:

```bash
python /evaluation/evaluator.py <optional_trajectory_file_path>
```

Note that the trajectory file path must be an absolute path to the trajectory
file. There is no specific requirement on the trajectory file's content and format,
but it MUST record all steps conducted by the examinee (no matter it's agent or
human being). Benchmark users are allowed to inspect checkpoint rubrics to ensure
the trajectory contains all necessary information used in graders, but examinees
(e.g. agents) are not allowed to read checkpoint rubrics or evaluation code.

Note that trajectory file is optional. It is often used to grant partial credits.