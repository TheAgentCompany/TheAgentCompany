# How to launch your NPC
## Build the base image
* Make sure you use the latest main branch
* Go [base image folder](../base_image/)
* Replace `ENV OPENAI_API_KEY <YOUR OPENAI KEY>` with your openai api key. Currently only support openai model, defualt model is `gpt-4-turbo`
* Run `make build` in base image folder

## Build your own image
* Create a `scenarios.josn` file under your task folder. Each item represents a NPC. The key is full name which should matched name [here](./npc/npc_credential.json). For more information about NPC roles, check [here](../../servers/rocketchat/npc/npc_definition.json). For example, the `extra_info` should be the information that every can know, the `strategy_hint` should be the information only this NPC should know :
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

* `make build` in your folder
* `make run` in your folder, then you will run the task image and step into the container.
* Maunally execute `/utils/init.sh` then NPC will be launched, you will see the CMD output like below:

```
root@299afff5d411:/utils# ls
dependencies.yml  evaluator.py  init.sh  llm_evaluator.py
root@299afff5d411:/utils# sh init.sh 
+ ping -c 1
+ grep PING
+ awk -F[()] {print $2}
ping: usage error: Destination address required
+ SERVICE_IP=
+ echo  theagentcompany.com
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

## How to debug our NPC
* If your NPC not work as your expected, attach into your task container, when execute `init.sh`, the log will contain the command to launch a single NPC like below, the `agent_name` will decide which NPC get launched: 
`OPENAI_API_KEY=<YOUR OPENAI API KEY> python_default /npc/run_one_npc.py --agent_name="Liu Qiang"`
* It will show the log output of your NPC. `No message received, waiting...` means NPC are waiting for message. If received, it will print the message and the response.


## NOTE
* Remember to delete your openai api key in dockerfile before commit code.

# Depracted (You don't need to check the following doc, unless you know what you want)
# Solution 1: How to run dockerfile
1. Set the correct configuration
    1. Set the `OPENAI_API_KEY`. You should use your own key.
    2. Set the `REDIS_OM_URL` as you want. We already host it on ogma server. You can use the default value
    3. Set `BOT_URL` as the rocketchat URL. We already host it on ogma server. You can use the default value
    4. Set `BOT_NAME` and `BOT_PASSWORD` as the NPC you want to simulate.
    5. Change the `scenarios.json` file to your customized setting. See here for [guideline](./NPC_GUIDELINE.md).
    6. TODO: We will working on provide more predefined NPCs for choice

The following is a dockerfile example, you can use it build a npc example and run it.
```Dockerfile
FROM base-image
# Step1: Set ENV: OPENAI API KEY, REDIS_OM_URL, BOT_URL
ENV OPENAI_API_KEY <Your OPENAI_API_KEY>
# Redis Username: default, Password: jobbench
# Redis service URL: theagentcompany.com/:6379
ENV REDIS_OM_URL redis://default:jobbench@theagentcompany.com/:6379
# RocketChat service URL
ENV BOT_URL http://theagentcompany.com:3000

# Step2: Change the scenarios.json to use your own definition
COPY scenarios.json /npc
# Step3: Execute the run_multi_npc.py in npc directory. Pay attention you need to execute it under /npc, we already configure the file path env in base-npc-image
#        If you also have other command to execute, put python run_multi_npc.py and others into scripts. Dockerfile only allow one CMD
#        run_multi_npc.py will launch the npc in backgroud then exit. In example, we sleep to keep docker running. You don't need to do it in examinee
CMD python /npc/run_multi_npc.py && sleep 1000000
```

# Solution 2: How to run code locally
## python environment
```
conda create -n bridge python=3.11; conda activate bridge;  
# option 1: use peotry
curl -sSL https://install.python-poetry.org | python3
poetry install
# option 2: use pip
pip install sotopia=="0.1.0-rc.1"
```

## OPENAI_API_KEY

OpenAI key is required to run the code. Please set the environment variable `OPENAI_API_KEY` to your key. The recommend way is to add the key to the conda environment:
```bash
conda env config vars set OPENAI_API_KEY=your_key
```

## Redis
You can directly launch the server docker compose file. We already config the redis server there. Port is 8092, username is `jobbench` and password is `jobbench`

If you don't want to use it, you can config it follow this doc for linux.

A redis-stack server is required to run the code.
Here are four lines of code to create a redis-stack server:
```bash
curl -fsSL https://packages.redis.io/redis-stack/redis-stack-server-7.2.0-v10.focal.x86_64.tar.gz -o redis-stack-server.tar.gz
tar -xvf redis-stack-server.tar.gz
pip install redis
echo -e "port 8092\nrequirepass jobbench\nuser jobbench on >jobbench ~* +@all" > redis-stack-server.conf
./redis-stack-server-7.2.0-v10/bin/redis-stack-server redis-stack-server.conf --daemonize yes
```

The `REDIS_OM_URL` need to be set before loading and saving agents:
```bash
conda env config vars set REDIS_OM_URL="redis://user:password@host:port"
# For example
conda env config vars set REDIS_OM_URL="redis://jobbench:jobbench@localhost:8092"
```

## Usage

```bash
python run.py
```

## Reference
### RocketChat bot Python package
We copy code from [here](https://github.com/jadolg/RocketChatBot).
Do little refactor to solve bug.
You can call `RocketChatBot` to use.

## RocketChat bot Node.JS package
See [here](https://developer.rocket.chat/docs/develop-a-rocketchat-sdk-bot) for instuction.
