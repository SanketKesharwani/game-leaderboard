from django.test import TestCase
from unittest.mock import patch
from apis.services.ranking_service import get_user_rank
from apis.models.user import User

class RankingServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="rankuser")

    @patch("apis.services.ranking_service._redis_client")
    def test_get_user_rank_with_score(self, mock_redis):
        mock_redis.zscore.return_value = 150
        mock_redis.zrevrank.return_value = 0
        result = get_user_rank(self.user.id)
        self.assertEqual(result["user_id"], self.user.id)
        self.assertEqual(result["username"], self.user.username)
        self.assertEqual(result["total_score"], 150)
        self.assertEqual(result["rank"], 1)

    @patch("apis.services.ranking_service._redis_client")
    def test_get_user_rank_no_score(self, mock_redis):
        mock_redis.zscore.return_value = None
        result = get_user_rank(self.user.id)
        self.assertEqual(result["total_score"], 0)
        self.assertIsNone(result["rank"])

    def test_get_user_rank_user_not_found(self):
        with self.assertRaises(ValueError):
            get_user_rank(999) 