# NPC (Non-Player Character)

Target audience of this doc: benchmark developers that would like to incorporate NPCs in their tasks.

## How to start NPC

### Step 1: Create NPC accounts in RocketChat

NOTE: If you want to use an existing NPC that is already in
[npc_credential.json](../../base_image/npc_credential.json), you can skip this step.

Otherwise, if you'd like to create a new NPC account, please do so in the hosted RocketChat service.
As of now, this is a manual step that you have to do via web GUI. Please then add
the username and password to [npc_credential.json](../../base_image/npc_credential.json)
using the following format:

```json
 "<First Name>" : {
        "username": "<username>",
        "password": "<password>"
    },
```

where `<First Name>` MUST be unique. It is used as a global identifier which is
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

### Step 3: Define the NPC involved in this task

In this directory, we provide an example for you. You can directly run it.

When try to build your own customized image:
* Set your openai api key `Dockerfile`.
* Change `scenarios.json`, each line will launch a sotopia NPC. The key is first name, the value is the instruction for NPC.

## NPC rules

* Keep data consistent. The user registed in rocketchat, and the NPC information in redis should match. Especially the name!
* When run one NPC, NPC will reply only when your send massage. It will talk with you TURN by TURN
* When multiple NPC in one channel, they will only reply your message. NPC cannot talk with each other in channel. If you send one message, all NPC will reply you. We can let only related agent reply. It is feasible, but not support now. Unless you need this feature, or just keep design concise.
* One NPC can run great now. Because of above problem. Unless neccessary in your task, don't use multiple NPC.
* Direct message multiple NPC will not cause mess. It run great now.
* Do fine-grained control on NPC prompt, message filter are feasible. But you need to impelement it and build customized image by yourself.
* In the end, we want to make NPC definition and NPC credential keep consistency and reused globally.
