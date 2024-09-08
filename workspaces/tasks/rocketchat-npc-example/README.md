# How to run dockerfile
1. change the `OPENAI_API_KEY` in dockerfile
2. `make build`
3. `make run`

# How to run code locally
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
conda env config vars set REDIS_OM_URL="redis://jobbench:jobbench@localhost:8092"
```

## Usage

```bash
python run.py
```


# How to run RocketChat simple example without NPC 
## Python package
We copy code from [here](https://github.com/jadolg/RocketChatBot).
Do little refactor to solve bug.
You can call `RocketChatBot` to use.

## How to launch Node.JS version
See [here](https://developer.rocket.chat/docs/develop-a-rocketchat-sdk-bot) for instuction.
