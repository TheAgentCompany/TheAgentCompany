# NPC (Non-Player Character)

Target audience of this doc: benchmark developers that would like to incorporate NPCs in their tasks.

## How to start NPC

### Step 1: Register the NPC in rocketchat
NOTE: If you want to use an existing user in [npc_credential.json](../../base_image/npc_credential.json), you can skip this step.

Make sure you already create the NPC account in rocketchat. In [npc_credential.json](../../base_image/npc_credential.json), you should create records for username and password. The Key is first name. All data are case sensitive.

### Step 2: Populate NPC definition in Redis
NOTE: If you already populate the NPC data, or use an existing NPC definition, you can skip this step.

In [populate_data.py](../../../servers/rocketchat/npc/populate_data.py), we define the agent definitons. Execute the code, all data will popuate into redis. Pay attention, this data should match with NPC first name in rocketchat.

### Step 3: Build base-npc-image
If you changed [npc_credential.json](../../base_image/npc_credential.json), you should rebuild it. Go `rocketchat-npc` directory and run `make build`

### Step 4: Define the NPC you want to involve
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
