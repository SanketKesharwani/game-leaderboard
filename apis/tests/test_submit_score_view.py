from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth.models import User

class SubmitScoreViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/v1/leaderboard/submit/"

    @patch("apis.views.submit_score_view.submit_score")
    def test_valid_score_submission(self, mock_submit_score):
        mock_submit_score.return_value = (150, 2)
        data = {"user_id": self.user.id, "score": 150, "game_mode": "solo"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["new_total"], 150)
        self.assertEqual(response.data["rank"], 2)

    def test_invalid_score_submission(self):
        data = {"user_id": self.user.id, "score": -10, "game_mode": "solo"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apis.views.submit_score_view.submit_score") 
    def test_user_not_found(self, mock_submit_score):
        mock_submit_score.side_effect = ValueError("User with ID 999 does not exist")
        data = {"user_id": 999, "score": 10, "game_mode": "solo"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)