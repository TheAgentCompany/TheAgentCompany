## Benchmarking Guidelines

Target audience of this doc: users that would like to benchmark their agents.

Make sure you have all services launched and running before you start evaluation.
This guideline uses [OpenHands](https://github.com/All-Hands-AI/OpenHands) and
[Example](./workspaces/tasks/example) task. The exact steps might differ among various agents and actual human beings,
but the general principles should hold.

### Step 0: Launch All Services

Please refer to [servers README](./servers/README.md) for instructions.
In the future we will make this step as automated as possible.

### Step 1: Build Base Image

This step only needs to be done once across all tasks. It builds a base image
that can be used by all exam (task) images.

```bash
docker build -t base-image workspaces/base_image --no-cache
```

### Step 2: Build Exam Image

An exam image is the image used for a specific task. It can be built via:

```bash
docker build -t example-exam-image workspaces/tasks/example --no-cache
```

An examinee should finish all its work in a container created out of this image.
The built container is analagous to a laptop used in an interview or daily work.

Note that the task image is guaranteed to NOT have any `RUN` or `ENTRYPOINT` instruction, but
it MAY contain an initialization script `/utils/init.sh`.  As a benchmark user
(e.g. you are the one who'd like to evaluate an agent), you should run

```bash
bash /utils/init.sh
```

After you start the container and before you let the examinee start the task.

### Step 3: Launch Agent

This step varies among examinees. We use OpenHands, a platform for software development
agents powered by AI.

OpenHands requires a sandbox environment that the agent needs to run in. It allows
users to provide a custom sandbox image, and thus we will use the `example-exam-image`
we just built.

Note: we are working on a programmatic evaluation harness to run
the benchmark with OpenHands automatically. As of now, you'd need
to run OpenHands manually as follows.

Clone `OpenHands` repo and create a `config.toml` in the OpenHands directory:

```toml
[core]
workspace_base="/workspace"
run_as_openhands=true
sandbox_base_container_image="example-exam-image"
```

Please note you also need to add LLM keys to `config.toml`. Please follow OpenHands
documentation to complete the setup.

Finally, you could now prompt the agent running on OpenHands with the task.
You could prompt the agent with, say,

> Complete the task in /instruction/task.md


### Step 4: Run Evaluation

Once the examinee has finished its work (as of now, we don't enforce timing),
run the below command in the exam container to grade the exam:

```bash
python_default /utils/evaluator.py <optional_trajectory_file_path>
```

Note that the trajectory file path must be an absolute path to the trajectory
file. There is no specific requirement on the trajectory file's content and format,
but it MUST record all steps conducted by the examinee (no matter it's agent or
human being). Benchmark users are allowed to inspect checkpoint rubrics to ensure
the trajectory contains all necessary information used in graders, but examinees
(e.g. agents) are not allowed to read checkpoint rubrics or evaluation code.

Note that trajectory file is optional. It is often used to grant partial credits.