# How to run Python package
We copy code from [here](https://github.com/jadolg/RocketChatBot).
Do little refactor to solve bug.
You can call `RocketChatBot` to use.

# How to launch Node.JS version
See [here](https://developer.rocket.chat/docs/develop-a-rocketchat-sdk-bot) for instuction.

# sotopia-bridge
Connect sotopia with matterbridge

## Getting Started

```
conda create -n bridge python=3.11; conda activate bridge;  curl -sSL https://install.python-poetry.org | python3
poetry install
```


You need to have a pre-exposed [API](https://github.com/42wim/matterbridge/wiki/Api) from matterbridge to use this agent.
(Basically if you are in this project, you should ask for the API)

OpenAI key is required to run the code. Please set the environment variable `OPENAI_API_KEY` to your key. The recommend way is to add the key to the conda environment:
```bash
conda env config vars set OPENAI_API_KEY=your_key
```

A redis-stack server is required to run the code.
Here are four lines of code to create a redis-stack server:
```bash
curl -fsSL https://packages.redis.io/redis-stack/redis-stack-server-7.2.0-v10.focal.x86_64.tar.gz -o redis-stack-server.tar.gz
tar -xvf redis-stack-server.tar.gz
pip install redis
./redis-stack-server-7.2.0-v10/bin/redis-stack-server --daemonize yes
```

The `REDIS_OM_URL` need to be set before loading and saving agents:
```bash
conda env config vars set REDIS_OM_URL="redis://user:password@host:port"
```
## Set up the matterbridge API
You also need to set up the matterbridge API:
Download binary from `https://github.com/42wim/matterbridge/releases/tag/v1.26.0`. E.g.,

```bash
cd matterbridge; wget https://github.com/42wim/matterbridge/releases/download/v1.26.0/matterbridge-1.26.0-linux-64bit
```

There is the configuration file `matterbridge.toml` under folder `matterbridge`, and then inside the folder run `./matterbridge-1.26.0-linux-64bit` to start the bridge.

## Usage

```bash
python run.py
```
