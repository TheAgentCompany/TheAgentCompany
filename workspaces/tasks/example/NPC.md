# NPC (Non-Player Character)

Target audience of this doc: benchmark developers that would like to incorporate NPCs in their tasks.

## Existing NPCs and Channels
You to use existing NPCs and channels when creating the tasks.

Here are the existing channels

| Name               | Users | Created At       |
|--------------------|-------|------------------|
| engineering        | 2     | October 11, 2024 |
| general            |       | October 19, 2024 |
| help-desk          | 14    | October 11, 2024 |
| hr-announcements   | 3     | October 11, 2024 |
| kudos              | 19    | October 11, 2024 |
| product            | 4     | October 11, 2024 |
| project-ai         | 6     | October 11, 2024 |
| project-graphdb    | 6     | October 11, 2024 |
| project-lowcode    | 5     | October 11, 2024 |
| project-search     | 5     | October 11, 2024 |
| project-streamdb   | 5     | October 11, 2024 |
| project-webcrawler | 6     | October 11, 2024 |
| random             | 8     | October 11, 2024 |
| sales-marketing    | 3     | October 11, 2024 |
| tech-talk          | 12    | October 11, 2024 |

Here are the existing NPCs and their channels:

| Name               | User Name         | Occupation                                  | Info                                                                                                                                                  | Channels                                            |
|--------------------|-------------------|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| Sarah Johnson      | sarah_johnson     | CTO                                         | Responsibilities: Technical strategy planning, R&D team leadership, new technology assessment; Project: Oversees all technical projects; Skills: N/A | All technical channels, #general, #tech-talk       |
| Li Ming            | li_ming           | Database Team Project Manager               | Responsibilities: Managing database projects, resource coordination, ensuring timely delivery; Project: JanusGraph (Graph Database); Skills: Java, distributed systems | #project-graphdb, #engineering, #tech-talk         |
| Zhang Wei          | zhang_wei         | Senior Software Engineer (Streaming DB Team)| Responsibilities: Developing and optimizing core streaming database functionalities; Project: RisingWave (Streaming Database); Skills: Rust, database systems | #project-streamdb, #engineering, #tech-talk        |
| Wang Fang          | wang_fang         | AI Researcher (AI Team)                     | Responsibilities: Designing and implementing machine learning models, optimizing model performance; Project: OpenHands (LLM project); Skills: Python, machine learning, LLM | #project-ai, #engineering, #tech-talk              |
| Mike Chen          | mike_chen         | Senior Software Engineer (AI Team)          | Responsibilities: Developing and optimizing LLM inference engines; Project: llama.cpp (LLM inference project); Skills: C++, CUDA, performance optimization | #project-ai, #engineering, #tech-talk              |
| Emily Zhou         | emily_zhou        | Software Engineer (Web Crawler Team)        | Responsibilities: Designing and implementing web crawler functionalities; Project: Colly (Web Crawler Framework); Skills: Go, distributed systems | #project-webcrawler, #engineering, #tech-talk      |
| Liu Qiang          | liu_qiang         | Quality Assurance Engineer                  | Responsibilities: Developing test strategies, executing tests, ensuring product quality; Project: All projects (focusing on testing and quality); Skills: N/A | All project channels, #engineering, #tech-talk     |
| Priya Sharma       | priya_sharma      | Documentation Engineer                      | Responsibilities: Writing technical documentation, maintaining wiki, improving documentation processes; Project: Documentation (Wiki); Skills: N/A | All project channels, #engineering, #tech-talk     |
| Mark Johnson       | mark_johnson      | Sales Director                              | Responsibilities: Developing sales strategies, managing sales team, expanding client relationships; Project: N/A (Sales); Skills: N/A | #sales-marketing, #general                         |
| Jessica Lee        | jessica_lee       | Marketing Manager                           | Responsibilities: Developing marketing strategies, managing brand image, organizing marketing events; Project: N/A (Marketing); Skills: N/A | #sales-marketing, #general                         |
| Chen Xinyi         | chen_xinyi        | Human Resources Manager                     | Responsibilities: Recruitment, employee training, compensation management; Project: N/A (HR); Skills: N/A | #hr-announcements, #general                         |
| David Wong         | david_wong        | Finance Director                            | Responsibilities: Financial planning, budget management, financial reporting; Project: N/A (Finance); Skills: N/A | #general                                            |
| Huang Jie          | huang_jie         | Product Manager (Search Engine Team)        | Responsibilities: Defining product requirements, planning product roadmap, communicating with clients; Project: OpenSearch (Search Engine); Skills: N/A | #project-search, #product, #tech-talk              |
| Sophia Rodriguez   | sophia_rodriguez  | UX Designer                                 | Responsibilities: Designing user interfaces, improving user experience, conducting user research; Project: All projects (focusing on user experience); Skills: N/A | All project channels, #product, #tech-talk         |
| Alex Turner        | alex_turner       | Software Engineer (Low-Code Platform Team)  | Responsibilities: Developing low-code platform features; Project: Node-RED (Low-Code Platform); Skills: N/A | #project-lowcode, #engineering, #tech-talk         |
| Emma Lewis         | emma_lewis        | Software Engineer (API Team)                | Responsibilities: Developing API functionalities using Python; Project: API-server; Skills: N/A | #engineering, #tech-talk                            |
| Jessica Chen       | jessica_chen      | Frontend Software Engineer                  | Responsibilities: Developing user interfaces, implementing responsive designs, optimizing web performance; Project: E-commerce Website Redesign; Skills: N/A | #project-ecommerce, #frontend, #tech-talk          |

## How to create new NPCs
If necessary, you can create new NPCs.

### Step 1: Create NPC accounts in RocketChat

NOTE: If you want to use an existing NPC that is already in
[npc_credential.json](../../base_image/npc_credential.json), you can skip this step.

Otherwise, if you'd like to create a new NPC account, please do so in the hosted RocketChat service.
As of now, this is a manual step that you have to do via web GUI. The idea is that
NPCs are like normal employees in the company and thus their RocketChat accounts
as well as their personalities are shared across all tasks.

After account crreation, please add the username and password to
[npc_credential.json](../../base_image/npc_credential.json)
in the following format:

```json
 "<first_name>" : {
        "username": "<username>",
        "password": "<password>"
    },
```

where `<first_name>` MUST be unique. It is used as a global identifier which is
also referenced in each individual task's `scenarios.json` and server's
[npc_definition.json](../../../servers/rocketchat/npc/npc_definition.json).
Everything in the credential file is case sensitive.

### Step 2: Populate NPC definition to Sotopia

NPCs are powered by [sotopia](https://github.com/sotopia-lab/sotopia/commits),
which stores NPCs' definitions in a Redis server.

NOTE: If you want to use an existing NPC, you can skip this step.

Otherwise, please add NPC definition in [npc_definition.json](../../../servers/rocketchat/npc/npc_definition.json)
and then run [populate_data.py](../../../servers/rocketchat/npc/populate_data.py)
on the server side to populate data into Redis. The script is designed to be idempotent.
The complete schema of NPC definition can be found in [NPC_CONFIG.md](../../../servers/rocketchat/npc/NPC_CONFIG.md).

### Step 3: Define the NPCs' context in this task

Write a `scenarios.json` like [this](./scenarios.json) that defines the NPCs
that may involve in the task, and their context.

## NPC rules

* Keep data consistent. Please make sure the `<first_name>` in `npc_credential.json`
matches the `first_name` field in `npc_definition.json` and the keys in `scenarios.json`.
* When run one NPC, NPC will reply only when your send massage. It will talk with you TURN by TURN
* When multiple NPC in one channel, they will only reply your message. NPC cannot talk with each other in channel. If you send one message, all NPC will reply you. We can let only related agent reply. It is feasible, but not support now. Unless you need this feature, or just keep design concise.
* One NPC can run great now. Because of above problem. Unless neccessary in your task, don't use multiple NPC.
* Direct message multiple NPC will not cause mess. It run great now.
* Do fine-grained control on NPC prompt, message filter are feasible. But you need to impelement it and build customized image by yourself.
* In the end, we want to make NPC definition and NPC credential keep consistency and reused globally.
