## Goal
Goal is to create a realistic, reproducible, executable benchmark and environment suite that tests agents' ability in performing tasks in professionals' work time from various fields, such as software engineers, designers, analyst, doctors, nurses and lawyers to name a few. 
Existing agent benchmark mostly focused on daily life scenarios, and cannot test the expert domain knowledge and complexities required in many professional tasks.

## Tasks

We have previously created a benchmark called WebArena for evaluating web agents on actual tasks that people perform in every-day life. 
In constructing WebArena, we took a semi-systematic approach of viewing the browsing history of the research team (students and faculty members in the CMU School of Computer Science) and choosing tasks that reflected the types of tasks that we did in our everyday life.

There are several obvious issues with this if we want to evaluate web agents with broader implications:
- Despite some grounding in realistic data, the process of creating tasks from this data was quite heuristic, and no consideration was made for how important or time consuming the tasks are.
- The tasks are biased towards those important for academics in computer science, and not reflective of tasks performed by the entire population
- They are more towards 

In this work, we plan on significantly expanding WebArena to a broader variety of tasks *motivated by tasks performed during real-world work*. 

We want to have a reproducible, generalized recipe for finding tasks to include in the benchmark is important to enable scalability given a new expert domain (in our case a new job/profession), since we want to find realistic tasks that are mostly unbiased, and originate from the real professionals rather than making things up ourselves with fields we are not familiar with.
That, as a part of the work's contribution, could justify the bias issues in task collection for domains that we are not an expert in.

We plan on referencing the O*NET database (https://www.onetonline.org/), which is a database of all the jobs performed by workers in the US created by the US Department of Labor. It also contains information about tasks performed within the context of each job, abilities required to perform each task, and other pieces of relevant information.
Followed by annotations by a group based on the task categories for software engineers, we crowdsourced the following tasks for initial study within Software Engineering jobs: https://docs.google.com/spreadsheets/d/1B_7Y80LFSDnKNZ-VUa7ueD5kd9gJhzOichnzhb_Ywsg/edit?usp=sharing


## Tools
We have decided with the following environment:
### Client-side tools:
- Cmd line - code, mock APIs, eval code, server, cluster, etc.
- Web Browser

### Server-side services:
- Internal documentation - wiki, or static pages
- Gitlab - code and for project management, etc.  
- Office suite, cloud drive - Owncloud


## Environments
- Fixed environments inside Docker containers for best reproducibility
- Live services for another suite of evaluations

## Observation and Actuation Modalities
For each task, we hope to provide the agents with as many modalities as possible for them to observe and actuate. We also try to compare the performance between using them, and possibly explore dynamically selecting the best for different scenarios.

- Image/video-based observation and pixel coordinate-based actuation: providing screenshot and pixels to the agent.
- XML/DOM/A11y tree-based observation and element-based actuation: providing raw html (webpage) or GUI layout (XML) to the agent.
- API-based interaction: providing API specifications and documentation (OpenAPI) to the agent, where agent could observe and actuate programatically.

The support for this part is mainly from the agent framework OpenHands (https://github.com/All-Hands-AI/OpenHands).

## Evaluators

- Execution-based evaluations: write programs to verify the final state, might be difficult for some tasks (e.g. plot a graph)
- Step-based evaluations: check the steps produced by the agents, possibly have partial scores.
- Checkpoint-based evaluations: have verifiable checkpoints along the way of more complex tasks, e.g. check if the website is live if the task involves starting up a server first.


## Baselines
- OpenHands included agent implementations.

## Human Evaluation and Trajectory Collection
- The tasks will be very challenging and thus how human perform the task will also be an important factor.
- Looking to incorporate some data collection techniques in plugins for web agents
- Screen recording, key logger, etc.
