import json

# Read JSON data from file
with open('models/models.json', 'r') as file:
    data = json.load(file)

# Extract active model IDs
active_models = [model["id"] for model in data["data"] if model["active"]]

def get_owner(model_id):
    for model in data["data"]:
        if model["id"] == model_id:
            return model["owned_by"]
    return None
