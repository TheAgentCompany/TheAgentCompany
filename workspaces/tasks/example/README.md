# Example Task

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
