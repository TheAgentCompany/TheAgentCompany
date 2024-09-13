# Example Task

Target audience: benchmark developers.

This is the documentation on how to create a task. In this doc we will be using
this folder as an example task. Other tasks shall not have this README file.

## Task (Full Intent)

Every task folder should have a `task.md` that describes the task. It shall not
contain detailed step-by-step guidelines unless absolutely necessary. It shall not
contain rubrics used for grading.

## Checkpoints (Evaluator)

Every task folder may have a `checkpoints.md` that documents the checkpoint rubrics.
This is optional, but strongly recommended.

Every task folder must have an `evaluator.py` that can be run to grade the
examinee's work. It must take exactly one CLI argument that is a path to the
trajectory file. There's no specific format requirement on the trajectory file,
but it MUST document the necessary steps conducted by the examinee.

## Build time (Dockerfile)

Every task folder should have a `Dockerfile` that will be used to build a container
where the examinee shall finish its task. Think of it as a PC environment you'd like
to provide your interviewee with. It is not required, but strongly recommended, to
build the image on top of the [base image](../../base_image/Dockerfile).

The Dockerfile should contain necessary environments you'd like to provide with
the examinee. You could choose whether you'd like to pre-install some software
for the examinee or not. Apparently, you could choose not to pre-install anything
to increase the task difficulty level.

The Dockerfile should install all dependencies your evaluator needs. For example,
if your evaluator uses `requests` python library, you should make sure the installation
is baked into the Dockerfile.

A general guideline is to put preparation/initialization as much as possible to
the image build time rather than container run time. The idea is to make task
container start-up time as short as possible. Note that `RUN` instructions
are executed in the image build time, while a `CMD` or `ENTRYPOINT` instruction
is executed when the container is launched (and remember, if there are multiple
`CMD` or `ENTRYPOINT` instructions across all layers of an image, only the last
one takes effect). For consistency, please DO NOT put any `CMD` or `ENTRYPOINT`
instructions into the task Dockerfile.

## Run time (init scripts, optional)

The example task contains `init.sh`, which calls `pre_init.py` and `post_init.py`.
These are optional and you only need them if you need to set up some environments,
or run sanity checks. If you, for example, attempt to launch an HTTP server that
is needed by the examinee, you shall put it as part of `init.sh`.

`pre_init.py` and `post_init.py` are optional. You could remove them or rewrite
them as shell scripts or any other executable. A common use case for `pre_init.py`
is to check whether services involved in the task are ready and in a clean state.
For example, it could check access to a wiki page, check existence 
of some repository, issue, pull request in GitLab, and check existence of an user in
RocketChat. If sanity checks fail, it could either fail the whole container, or
attempt to fix them.

A common use case for `post_init.py` is to validate the initialization process.
For example, in the task image, initialization step launches NPC(s). Post-init
step could check if the OpenAI key is valid and NPCs are working. If not, it
would fail the container.

Benchmark developers only need to provide the `init.sh`, but not execute them
as part of `RUN` or `ENTRYPOINT` instructions in the Dockerfile. It is benchmark users'
responsibility to run them before the examinee starts its task. The reason is some
agent frameworks might choose to override `CMD` or `ENTRYPOINT` instruction in
their customized images built on top of task images. For consistency and simplicitly,
it is required that all benchmark developers shall avoid including any runtime
instructions in their task Dockerfile.

## NPC (optional)

Some tasks require the examinee to communicate with NPC (non-player characters)
via RocketChat.

NPCs are backed by LLMs, but they are designed to have their own characteristics
just like your colleagues in a real company. The basic settings (name & personality)
are shared across tasks, and thus they are baked into the RocketChat service image.

However, different tasks might have different scenario settings. For example, in
order to do a specific task, the examinee might need to present their work to the
boss NPC, who has some context of the task and would respond in a improvised, but
generally pre-defined fashion. This context is defined in each individual task image.

If your task needs to involve NPCs, please see details [here](./NPC.md)

## prerequisite (Optional)
In `prerequisite.py`, it will check the local environment and the server environment.
The checkpoints are decide by your task. For example, access to a wiki page, check existence 
of some repository, issue, pull request in gitlab, check existence of user in rocketchat.
If the check pass, it means evnironment initialization state is clean. If fails, the server 
need to reset. You are not required to check every details. A general check may good enough to 
catch most errors. This file is not required, but encourage to have.
