## Workspace directory

This directory hosts workspaces that are local to the examinee (e.g. agents or actual human users).

Each task will have its own container image and related evaluation code, e.g. LLM-based evaluation or end-to-end tests.

Highlights:
- `base_image` folder contains artifacts needed to build the base image. All tasks'
images are based on the base image.
- `tasks\example` folder contains a simple example task that demonstrates what a task
looks like, and is a blueprint for creating more complicated tasks.