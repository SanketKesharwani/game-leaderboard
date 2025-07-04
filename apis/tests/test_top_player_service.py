from django.test import TestCase
from unittest.mock import patch
from apis.services.top_player_service import get_top_n_players
from apis.models.user import User

class TopPlayerServiceTest(TestCase):
    @patch("apis.services.top_player_service.redis_client")
    def test_get_top_n_players(self, mock_redis):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        mock_redis.zrevrange.return_value = [
            (str(user1.id).encode(), 200),
            (str(user2.id).encode(), 100),
        ]
        result = get_top_n_players(2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["user_id"], user1.id)
        self.assertEqual(result[1]["user_id"], user2.id)
        self.assertEqual(result[0]["total_score"], 200)
        self.assertEqual(result[1]["total_score"], 100)

    @patch("apis.services.top_player_service.redis_client")
    def test_get_top_n_players_empty(self, mock_redis):
        mock_redis.zrevrange.return_value = []
        result = get_top_n_players(5)
        self.assertEqual(result, []) 