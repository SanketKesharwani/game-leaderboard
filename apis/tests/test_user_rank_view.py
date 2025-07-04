from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth.models import User

class UserRankViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = f"/api/v1/leaderboard/rank/{self.user.id}/"

    @patch("apis.views.user_rank_view.get_user_rank")
    def test_get_user_rank(self, mock_get_rank):
        mock_get_rank.return_value = {"user_id": self.user.id, "username": self.user.username, "total_score": 100, "rank": 1}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["rank"], 1)

    @patch("apis.views.user_rank_view.get_user_rank")
    def test_user_not_found(self, mock_get_rank):
        mock_get_rank.side_effect = ValueError("User with id 999 does not exist")
        url = "/api/v1/leaderboard/rank/999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 