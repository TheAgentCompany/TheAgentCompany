# Example Task

Target audience: benchmark developers.

This is the documentation on how to create a task. In this doc we will be using
this folder as an example task. Other tasks shall not have this README file.

## Task (Full Intent)

Every task folder should have a `task.md` that describes the task. It shall not
contain detailed step-by-step guidelines unless absolutely necessary. It shall not
contain rubrics used for grading.

## Checkpoints (Evaluator)

Every task folder should have a `checkpoints.md` that documents the checkpoint rubrics.

Every task folder must have an `evaluator.py` that can be run to grade the
examinee's work. The `evaluator.py` must not have a main function. Instead, it
must have a `grade_checkpoints` function that returns a `Result` object.

Here's an example, which you can also find in this example task's `evaluator.py`:

```python
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_final_checkpoint()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result
```

`Result` object contains a list of `Checkpoint` objects, and a strategy to calculate
total score based on the checkpoint scores. By default, the strategy is to sum up
all checkpoint scores. However, benchmark developers can customize the formula
by providing their customized strategy. In `base_image/scoring.py` you can find
two pre-defined strategies: `bonus_for_completing_any` and `bonus_for_completing_all`.

* `bonus_for_completing_any` awards full credit for the 1st checkpoint if any of the checkpoints is passed. 
* `bonus_for_completing_all` awards full credit for the entire task if the last checkpoint is passed. 

In the example task, we use the
`bonus_for_completing_all` strategy, because as long as the examinee has passed
the final checkpoint, it means they completed the entire task. Those strategies
are commonly used in tasks where there's more than one approach to complete the
task, OR when some checkpoints use trajectory file for validation.

Note that `common.py` contains a decorator, `@checkpoint`, which can be used to
annotate each individual `grade_checkpoint[X]` function. This is required as it
would capture runtime errors and make the evaluator not fail the entire task.
Annotated checkpoint functions would return `False` if any runtime error occurs,
and is not already captured by the checkpoint function itself.  CI would fail if
there's no checkpoint annotator in the entire `evaluator.py`.

### Trajectory file

Some tasks require the examinee to conduct a series of steps, but not every step
can be validated easily. For example, whether the examinee has accessed a web page
is hard to validate programmatically. In this case, it is okay for benchmark developers
to validate the trajectory file that documents the steps conducted. For example,
whether a specific URL appears in the trajectory file.

There's no specific format requirement on the trajectory file,
but it MUST document the necessary steps conducted by the examinee. A trajectory
file usually includes the URLs accessed, the commands run, the files modified, etc.

Note: benchmark developers shall use the trajectory file as the last resort.

## Build time (Dockerfile)

Every task folder should have a `Dockerfile` that will be used to build a container
where the examinee shall finish its task. Think of it as a PC environment you'd like
to provide your interviewee with. It is required to
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

## Dependency config (dependencies.yml)

`dependencies.yml` is a mandatory file that records the service dependencies of
a task. For efficiency purpose, benchmark users are not required to reset all service
states between task runs - they only need to reset services that are needed by the
task. If your task doesn't rely on any service, simply put an empty `dependencies.yml`
file.

## Run time (init scripts, optional)

The base image contains `init.sh`, which calls `pre_init.py` and `post_init.py`
if they exist. You could choose to provide `pre_init.py` and/or `post_init.py`
in your task directory if you need to set up some uncommon environments,
or run non-standard sanity checks. If you, for example, attempt to launch an
HTTP server that is needed by the examinee, you could put it either in `pre_init.py`
or `post_init.py`.

A common use case for `pre_init.py`
is to check whether services involved in the task are ready and in a clean state.
For example, it could check access to a wiki page, check existence 
of some repository, issue, pull request in GitLab, and check existence of an user in
RocketChat. If sanity checks fail, it could either fail the whole script, or
attempt to fix/reset the environment.

A common use case for `post_init.py` is to validate the initialization process.
For example, in the task image, initialization step launches NPC(s). Post-init
step could check if the OpenAI key is valid and NPCs are working. Another common
scenario is the initialization process might involve some task-specific data population
steps. Post-init step could check if the data is correctly populated to the task
container. If not, it could choose to fail the script.

Note that `init.sh` is not executed as part of image build process. It is benchmark users'
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

If your task needs to involve NPCs, take a look at the example task. In a nutshell,
all you need to do is to add a `scenarios.json` that documents the NPCs involved, their
knowledge and their settings. For details, see [here](./NPC.md).


## Gitlab (optional)
Some tasks require the examinee to push the code to the gitlab. So they need to 
figure out by themselves without providing the credential to them