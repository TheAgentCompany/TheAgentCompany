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

## Dockerfile

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
one takes effect).

## Initialization scripts (optional)

The example task contains an `init.py` and `init.sh`, and you can see they are
used in `RUN` instructions in the sample Dockerfile. These are optional and you
only need them if you need to set up some environments or pre-populate some data.
Remember, if you put them in `RUN` instructions, then they are only executed during
image build time, not container run time. If you, for example, attempt to launch
an HTTP server that is needed by the examinee, you shall put it as part of last
`CMD` or `ENTRYPOINT` instruction.

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