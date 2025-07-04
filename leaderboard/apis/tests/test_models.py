from django.test import TestCase
from apis.models.user import User
from apis.models.game_session import GameSession
from apis.models.leaderboard import Leaderboard
from django.utils import timezone

class UserModelTest(TestCase):
    def test_user_creation_and_str(self):
        user = User.objects.create(username="testuser")
        self.assertEqual(str(user), "testuser")
        self.assertIsNotNone(user.join_date)

class GameSessionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="sessionuser")

    def test_game_session_creation_and_str(self):
        session = GameSession.objects.create(
            user=self.user,
            score=1234,
            game_mode="solo",
            timestamp=timezone.now()
        )
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.score, 1234)
        self.assertEqual(session.game_mode, "solo")
        self.assertIn("sessionuser", str(session))
        self.assertIn("1234", str(session))

class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="leaderuser")

    def test_leaderboard_creation_and_str(self):
        leaderboard = Leaderboard.objects.create(
            user=self.user,
            total_score=9999,
            rank=1
        )
        self.assertEqual(leaderboard.user, self.user)
        self.assertEqual(leaderboard.total_score, 9999)
        self.assertEqual(leaderboard.rank, 1)
        self.assertIn("leaderuser", str(leaderboard))
        self.assertIn("9999", str(leaderboard))
        self.assertIn("#1", str(leaderboard)) 