# Solution 1: How to run dockerfile
1. Set the correct configuration
    1. Set the `OPENAI_API_KEY`. You should use your own key.
    2. Set the `REDIS_OM_URL` as you want. We already host it on ogma server. You can use the default value
    3. Set `BOT_URL` as the rocketchat URL. We already host it on ogma server. You can use the default value
    4. Set `BOT_NAME` and `BOT_PASSWORD` as the NPC you want to simulate.
    5. Change the `scenarios.json` file to your customized setting. See here for [guideline](./NPC_GUIDELINE.md).
    6. TODO: We will working on provide more predefined NPCs for choice
2. `make build`
3. `make run`

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
