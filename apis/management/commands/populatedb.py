from django.core.management.base import BaseCommand
from apis.models.user import User
from apis.models.game_session import GameSession
from apis.models.leaderboard import Leaderboard
from django.db import transaction
import random
from datetime import timedelta, datetime
from django.db import models

class Command(BaseCommand):
    help = "Populate users, game_sessions, and leaderboard tables"

    def handle(self, *args, **options):
        NUM_USERS = 1000000
        NUM_SESSIONS = 5000000

        self.stdout.write("Seeding users...")
        users = [User(username=f"user_{i+1}") for i in range(NUM_USERS)]
        User.objects.bulk_create(users, batch_size=10000)
        user_ids = list(User.objects.values_list('id', flat=True))

        self.stdout.write("Seeding game sessions...")
        sessions = []
        now = datetime.now()
        for _ in range(NUM_SESSIONS):
            user_id = random.choice(user_ids)
            score = random.randint(1, 10000)
            game_mode = random.choice(['solo', 'team'])
            timestamp = now - timedelta(days=random.randint(0, 364))
            sessions.append(GameSession(user_id=user_id, score=score, game_mode=game_mode, timestamp=timestamp))
            if len(sessions) >= 10000:
                GameSession.objects.bulk_create(sessions, batch_size=10000)
                sessions = []
        if sessions:
            GameSession.objects.bulk_create(sessions, batch_size=10000)

        self.stdout.write("Aggregating leaderboard...")
        Leaderboard.objects.all().delete()
        leaderboard_data = (
            GameSession.objects.values('user_id')
            .order_by()
            .annotate(total_score=models.Sum('score'))
            .order_by('-total_score')
        )
        leaderboard_entries = []
        for rank, entry in enumerate(leaderboard_data, start=1):
            leaderboard_entries.append(
                Leaderboard(user_id=entry['user_id'], total_score=entry['total_score'], rank=rank)
            )
        Leaderboard.objects.bulk_create(leaderboard_entries, batch_size=10000)

        self.stdout.write(self.style.SUCCESS("Database seeded.")) 