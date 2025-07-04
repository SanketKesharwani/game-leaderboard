from django.test import TestCase
from apis.serializers.score_serializer import LeaderboardEntrySerializer

class LeaderboardEntrySerializerTest(TestCase):
    def test_valid_data(self):
        data = {"user_id": 1, "username": "user1", "total_score": 100, "rank": 1}
        serializer = LeaderboardEntrySerializer(data)
        self.assertEqual(serializer.data["user_id"], 1)
        self.assertEqual(serializer.data["username"], "user1")
        self.assertEqual(serializer.data["total_score"], 100)
        self.assertEqual(serializer.data["rank"], 1)

    def test_null_rank(self):
        data = {"user_id": 2, "username": "user2", "total_score": 50, "rank": None}
        serializer = LeaderboardEntrySerializer(data)
        self.assertEqual(serializer.data["rank"], None) 