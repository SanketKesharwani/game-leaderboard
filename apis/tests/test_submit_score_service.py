from django.test import TestCase
from unittest.mock import patch, MagicMock
from apis.services.submit_score_service import submit_score
from apis.models.user import User
from apis.models.leaderboard import Leaderboard
from apis.models.game_session import GameSession

class SubmitScoreServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

    @patch("apis.services.submit_score_service.redis_client")
    def test_submit_score_new_user(self, mock_redis):
        mock_redis.zscore.return_value = 100
        mock_redis.zrevrank.return_value = 0
        total, rank = submit_score(self.user.id, 100, "solo")
        self.assertEqual(total, 100)
        self.assertEqual(rank, 1)
        self.assertTrue(Leaderboard.objects.filter(user=self.user).exists())
        self.assertTrue(GameSession.objects.filter(user=self.user).exists())
        mock_redis.zadd.assert_called()
        mock_redis.zscore.assert_called()
        mock_redis.zrevrank.assert_called()

    @patch("apis.services.submit_score_service.redis_client")
    def test_submit_score_existing_user(self, mock_redis):
        Leaderboard.objects.create(user=self.user, total_score=50, rank=1)
        mock_redis.zscore.return_value = 100
        mock_redis.zrevrank.return_value = 0
        total, rank = submit_score(self.user.id, 50, "duo")
        self.assertEqual(total, 100)
        self.assertEqual(rank, 1)
        leaderboard = Leaderboard.objects.get(user=self.user)
        self.assertEqual(leaderboard.total_score, 100)
        mock_redis.zadd.assert_called()

    def test_submit_score_user_not_found(self):
        with self.assertRaises(ValueError):
            submit_score(999, 10, "solo") 