# load_game.py

import json
import redis
from normalize import populate_cache  # ✅ Import it


# Connect to Redis (adjust host/port/db as needed)
r = redis.Redis(host='localhost', port=6379, db=0)

# Load game_data.json
with open('game_data.json', 'r') as f:
    game_data = json.load(f)

# Store it as a single JSON string in Redis
r.set('game_data', json.dumps(game_data))

print("✅ Game data successfully loaded into Redis.")

# ✅ Populate synonym cache
populate_cache()

print("✅ Game data and acronym cache loaded into Redis.")


