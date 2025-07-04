from django.test import TestCase
from apis.serializers.leaderboard_serializer import ScoreSubmissionSerializer

class ScoreSubmissionSerializerTest(TestCase):
    def test_valid_data(self):
        data = {"user_id": 1, "score": 100, "game_mode": "solo"}
        serializer = ScoreSubmissionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user_id"], 1)
        self.assertEqual(serializer.validated_data["score"], 100)
        self.assertEqual(serializer.validated_data["game_mode"], "solo")

    def test_invalid_score(self):
        data = {"user_id": 1, "score": -5, "game_mode": "solo"}
        serializer = ScoreSubmissionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("score", serializer.errors)

    def test_missing_fields(self):
        data = {"user_id": 1, "score": 10}
        serializer = ScoreSubmissionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("game_mode", serializer.errors) 