<a name="readme-top"></a>

<div align="center">
  <img src="./docs/images/TAC_logo.png" alt="Logo" width="200">
  <h1 align="center">The Agent Company: Benchmarking LLM Agents on Consequential Real World Tasks</h1>
</div>


<p align="center">
    <a href="https://www.python.org/">
        <img alt="Build" src="https://img.shields.io/badge/Python-3.12+-1f425f.svg?color=purple">
    </a>
    <a href="https://github.com/TheAgentCompany/TheAgentCompany/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
    </a>
</p>


Please refer to the [website](https://the-agent-company.com/) for more details.

## Overview
<div align="center">
  <img src="./docs/images/TAC_architecture.png">
</div>



Today we interact with computers on an everyday basis, be it life or work.
Today, many aspects of professional work can be done entirely with access to a computer and the Internet.
At the same time, thanks to improvements in large language models (LLMs), there has also been a rapid development in AI agents that interact with and affect change in their surrounding environments.
But how performant are AI agents 
To measure the progress of these LLM agents' performance on performing real-world professional tasks,
in this paper, we introduce tac, an extensible benchmark for evaluating AI agents that interact with the world in similar ways to those of a digital worker: by browsing the Web, writing code, running programs, and communicating with other coworkers.
We build a self-contained environment with internal web sites and data that mimics a small software company environment, and create a variety of tasks that may be performed by workers in such a company.
We test baseline agents powered by both closed API-based and open-weights language models (LMs), and find that with the most competitive agent, 24% of the tasks can be completed autonomously.
This paints a nuanced picture on task automation with LM agents -- in a realistic setting simulating a real workplace, a good portion of simpler tasks could be solved autonomously, but more difficult long-horizon tasks are still beyond the reach of current systems.

## Set Up
Check out the [docs](./docs/SETUP.md) for more details.

## Exciting Features

- Diverse task roles:
  - Software Engineer
  - Product Manager
  - Data Scientist
  - Human Resource
  - Financial Staff
  - Administrator
- Diverse data types:
  - Coding tasks
  - Conversational tasks
  - Mathematical reasoning
  - Image processing
  - Text comprehension
- Multiple Agent Interaction
- Comprehensive scoring system
  - Result-based evaluation (primary)
  - Subcheckpoints checking (secondary)
- Multiple evaluation methods:
  - Deterministic evaluators
  - LLM-based evaluators
- Simple one-command operations:
  - Complete environment setup in minutes
  - Quick system reset in minutes when needed
- Extensible benchmark framework
  - Add new tasks/evaluators/subcheckpoints in minutes


# Contribution
We welcome any contributions to bug fixes, documentation, and other improvements.
Questions? Please create an issue. Otherwise, you can also contact [Frank F. Xu](https://frankxfz.me/), [Yufan Song](https://github.com/yufansong), [Boxuan Li](https://github.com/li-boxuan) (Email: fangzhex@cs.cmu.edu, yufans@alumni.cmu.edu, boxuanli@alumni.cmu.edu)

## Cite
TODO

## License
Distributed under the [MIT](./LICENSE) License. See LICENSE for more information.
