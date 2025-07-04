from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch

class TopLeaderboardViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/leaderboard/top/"

    @patch("apis.views.top_leaderboard_view.get_top_n_players")
    def test_get_top_leaderboard(self, mock_get_top):
        mock_get_top.return_value = [
            {"user_id": 1, "username": "user1", "total_score": 100, "rank": 1},
            {"user_id": 2, "username": "user2", "total_score": 80, "rank": 2},
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["user_id"], 1)

    @patch("apis.views.top_leaderboard_view.get_top_n_players")
    def test_get_top_leaderboard_empty(self, mock_get_top):
        mock_get_top.return_value = []
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, []) 