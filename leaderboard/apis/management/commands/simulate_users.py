import requests
import random
import time
from django.core.management.base import BaseCommand
from apis.utils.command import LeaderboardCommand

API_BASE_URL = "http://127.0.0.1:8000/api/v1/leaderboard"
JWT_TOKEN_URL = "http://127.0.0.1:8000/api/v1/auth/login/"
USERNAME = "admin"
PASSWORD = "admin"

def get_jwt_token():
    response = requests.post(JWT_TOKEN_URL, data={"username": USERNAME, "password": PASSWORD})
    response.raise_for_status()
    return response.json()["access"]

def submit_score(user_id, headers):
    score = random.randint(1000, 10000)
    game_mode = random.choice(["solo", "team"])
    requests.post(
        f"{API_BASE_URL}/submit/",
        json={"user_id": user_id, "score": score, "game_mode": game_mode},
        headers=headers
    )

def get_top_players(headers):
    response = requests.get(f"{API_BASE_URL}/top/", headers=headers)
    return response.json()

def get_user_rank(user_id, headers):
    response = requests.get(f"{API_BASE_URL}/rank/{user_id}/", headers=headers)
    return response.json()

class SimulateUsersCommand(LeaderboardCommand):
    def execute(self):
        import random
        import time
        token = get_jwt_token()
        headers = {"Authorization": f"Bearer {token}"}
        while True:
            user_id = random.randint(30,40)
            submit_score(user_id, headers)
            print(get_top_players(headers))
            print(get_user_rank(user_id, headers))
            time.sleep(1)

class Command(BaseCommand):
    help = 'Simulates users submitting scores and prints leaderboard updates.'
    def handle(self, *args, **options):
        simulate_command = SimulateUsersCommand()
        simulate_command.execute()