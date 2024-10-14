import json
import logging
from redis_om import Migrator, Field
from sotopia.database import AgentProfile
import time
import redis

class NPCDefinition(AgentProfile):
    slack_channels: str = Field(index=False, default_factory=lambda: "")

def wait_for_redis(host='localhost', port=6379, password='jobbench', retries=300, delay=1):
    client = redis.StrictRedis(host=host, port=port, password=password)
    
    for attempt in range(retries):
        try:
            # Test if Redis is responding to PING command
            if client.ping():
                print("Redis is up and running!")
                return True
        except redis.exceptions.ConnectionError:
            print(f"Attempt {attempt + 1} failed: Redis not available yet, retrying in {delay} seconds...")
            time.sleep(delay)
    
    print("Failed to connect to Redis after several retries.")
    return False

# NOTE: redis-stack are used to work with the dockerfile in server root path. It is a network shared with redis-stack
#       If you run locally, you can use the localhost
#       If you manually run this docker, you can remove this check if you are sure redis docker is running
wait_for_redis(host="redis-stack")

Migrator().run()

with open('npc_definition.json', 'r') as file:
    agent_definitions = json.load(file)
    print(f"NPC definitions loaded, number of NPCs = {len(agent_definitions)}")

def get_by_name(first_name, last_name):
    return NPCDefinition.find(NPCDefinition.first_name == first_name and NPCDefinition.last_name == last_name).execute()

for definition in agent_definitions:
    if get_by_name(definition["first_name"],definition["last_name"]):
        # TODO: shall we support modifications?
        print(f'NPC ({definition["first_name"]} {definition["last_name"]}) already inserted, skip')
        continue
    agent_profile = NPCDefinition.parse_obj(definition)
    agent_profile.save()
    print(f'Inserted {definition["first_name"]} {definition["last_name"]} successfully')
