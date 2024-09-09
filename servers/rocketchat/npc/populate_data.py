from redis_om import JsonModel, Migrator
from sotopia.database import AgentProfile

Migrator().run()


agent_definitions = [
    {
        "first_name": "X",
        "last_name": "AI",
        "occupation": "AI Assistant",
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "occupation": "Software Engineer",
    }
]


def get_by_first_name(first_name):
    return AgentProfile.find(AgentProfile.first_name == first_name).execute()

for definition in agent_definitions:
    if get_by_first_name(definition["first_name"]):
        print("Already inserted, skip")
        continue
    agent_profile = AgentProfile.parse_obj(definition)
    agent_profile.save()
    print("Inserted ", definition["first_name"] ," successfully")

for definition in agent_definitions:
    print(get_by_first_name(definition["first_name"]))
