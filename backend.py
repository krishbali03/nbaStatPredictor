from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StatsRequest(BaseModel):
    player: str
    stats: dict 

def get_player_data(player_name):
    player_name = player_name.strip().title()
    r = requests.get(f"https://www.balldontlie.io/api/v1/players?search={player_name}")
    results = r.json()['data']
    if not results:
        return {}
    player_id = results[0]['id']

    stats_r = requests.get(f"https://www.balldontlie.io/api/v1/stats?player_ids[]={player_id}&per_page=1")
    stats_data = stats_r.json()['data'][0]

    return {
        "points": stats_data['pts'],
        "rebounds": stats_data['reb'],
        "assists": stats_data['ast'],
        "fg_pct": stats_data['fg_pct']
    }

def calculate_probability(stats):
    return min(1.0, sum(stats.values()) / 100)

@app.get("/")
def root():
    return {"message": "Backend is running!"}

@app.post("/predict")
def predict(data: StatsRequest):
    player_data = get_player_data(data.player)
    if not player_data:
        return {"error": "Player not found"}

    selected_stats = {k: v for k, v in player_data.items() if data.stats.get(k)}
    probability = calculate_probability(selected_stats)

    return {
        "player": data.player,
        "selected_stats": selected_stats,
        "probability": probability
    }
