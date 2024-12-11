# How to Launch Your NPC

## Build the Base Image

* Make sure you are using the latest main branch.
* Navigate to the [base image folder](../base_image/).
* Set the following environment variables:
```
ENV LITELLM_API_KEY <YOUR LITELLM_API_KEY>
ENV LITELLM_BASE_URL <YOUR LITELLM_BASE_URL>
ENV LITELLM_MODEL <YOUR LITELLM_MODEL>
```
A good example is:
```
ENV LITELLM_API_KEY <YOUR OPENAI API KEY>
ENV LITELLM_BASE_URL https://api.openai.com/v1
ENV LITELLM_MODEL gpt-4o
```

* Run `make build` in the base image folder.

## Build Your Task Image

* Create a `scenarios.json` file in your task folder. Each item in this file represents an NPC.
* The key should be the full name of the NPC, which must match the name in [this file](./npc/npc_credential.json).
* For more information about NPC roles, check [this file](../../servers/rocketchat/npc/npc_definition.json).
* In the `scenarios.json` file:
  - The `extra_info` field is information that the NPC may share with others.
  - The `strategy_hint` field is private information that the NPC will use to act in a certain way.

```
{
  "Emily Zhou": {
    "extra_info": "Someone will ask you for your free time for the meeting",
    "strategy_hint": "You're available on Mondays, Wednesday, and Fridays. You're not available on all other week days."
  },
  "Liu Qiang": {
    "extra_info": "Someone will ask you for your free time for the meeting",
    "strategy_hint": "You're available on Tuesday, Thursday. You're not available on all other week days."
  }
}
```

# Launch NPC

* Run `make build` in your folder to build the task image.
* Execute `make run` in your folder. This will run the task image and bring you into the container.
* Manually execute `/utils/init.sh` inside the container. This will launch the NPC, and you will see output similar to the following:

```
root@299afff5d411:/utils# ls
dependencies.yml  evaluator.py  init.sh  llm_evaluator.py
root@299afff5d411:/utils# sh init.sh 
+ ping -c 1
+ grep PING
+ awk -F[()] {print $2}
+ SERVICE_IP=
+ echo  the-agent-company.com
+ [ -f /utils/pre_init.py ]
+ [ -f /npc/scenarios.json ]
+ python_default /npc/run_multi_npc.py
Launching Emily Zhou
OPENAI_API_KEY=<YOUR OPENAI API KEY> python_default /npc/run_one_npc.py --agent_name="Emily Zhou"
Launching Liu Qiang
OPENAI_API_KEY=<YOUR OPENAI API KEY> python_default /npc/run_one_npc.py --agent_name="Liu Qiang"
+ [ -f /utils/populate_data.py ]
+ [ -f /utils/post_init.py ]
```

## How to Debug Your NPC
* If your NPC is not working as expected, follow these steps:
  1. Attach to your task container.
  2. When executing `init.sh`, look for the command to launch a single NPC in the log output. It will look similar to this:
     ```
     OPENAI_API_KEY=<YOUR OPENAI API KEY> python_default /npc/run_one_npc.py --agent_name="Liu Qiang"
     ```
     The `agent_name` parameter determines which NPC gets launched.

* This command will display the log output of your NPC:
  - The message "No message received, waiting..." indicates that the NPC is waiting for a message.
  - When a message is received, the log will print both the incoming message and the NPC's response.

## Notes

* Important: Remember to remove your OpenAI API key from the Dockerfile before committing your code.
* Use `make stop` to halt and remove your previously running task image.

# Deprecated 
(You don't need to check the following documentation unless you know what you're looking for)

# Solution 1: How to run dockerfile
1. Set the correct configuration
    1. Set the `OPENAI_API_KEY`. You should use your own key.
    2. Set the `REDIS_OM_URL` as you want. We already host it on ogma server. You can use the default value
    3. Set `BOT_URL` as the rocketchat URL. We already host it on ogma server. You can use the default value
    4. Set `BOT_NAME` and `BOT_PASSWORD` as the NPC you want to simulate.
    5. Change the `scenarios.json` file to your customized setting. See here for [guideline](./NPC_GUIDELINE.md).

The following is a dockerfile example, you can use it build a npc example and run it.
```Dockerfile
FROM ghcr.io/theagentcompany/task-base-image:1.0.0
# Step1: Set ENV: OPENAI API KEY, REDIS_OM_URL, BOT_URL
ENV OPENAI_API_KEY <Your OPENAI_API_KEY>
# Redis Username: default, Password: theagentcompany
# Redis service URL: the-agent-company.com/:6379
ENV REDIS_OM_URL redis://default:theagentcompany@the-agent-company.com/:6379
# RocketChat service URL
ENV BOT_URL http://the-agent-company.com:3000

# Step2: Change the scenarios.json to use your own definition
COPY scenarios.json /npc
# Step3: Execute the run_multi_npc.py in npc directory. Pay attention you need to execute it under /npc, we already configure the file path env in base-npc-image
#        If you also have other command to execute, put python run_multi_npc.py and others into scripts. Dockerfile only allow one CMD
#        run_multi_npc.py will launch the npc in backgroud then exit. In example, we sleep to keep docker running. You don't need to do it in examinee
CMD python /npc/run_multi_npc.py && sleep 1000000
```

## OPENAI_API_KEY

OpenAI key is required to run the code. Please set the environment variable `OPENAI_API_KEY` to your key. The recommend way is to add the key to the conda environment:
```bash
conda env config vars set OPENAI_API_KEY=your_key
```

## Redis
You can directly launch the server docker compose file. We already config the redis server there. Port is 8092, username is `theagentcompany` and password is `theagentcompany`

If you don't want to use it, you can config it follow this doc for linux.

A redis-stack server is required to run the code.
Here are four lines of code to create a redis-stack server:
```bash
curl -fsSL https://packages.redis.io/redis-stack/redis-stack-server-7.2.0-v10.focal.x86_64.tar.gz -o redis-stack-server.tar.gz
tar -xvf redis-stack-server.tar.gz
pip install redis
echo -e "port 8092\nrequirepass theagentcompany\nuser theagentcompany on >theagentcompany ~* +@all" > redis-stack-server.conf
./redis-stack-server-7.2.0-v10/bin/redis-stack-server redis-stack-server.conf --daemonize yes
```

The `REDIS_OM_URL` need to be set before loading and saving agents:
```bash
conda env config vars set REDIS_OM_URL="redis://user:password@host:port"
# For example
conda env config vars set REDIS_OM_URL="redis://theagentcompany:theagentcompany@localhost:8092"
```
