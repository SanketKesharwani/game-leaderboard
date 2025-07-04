from django.urls import path
from apis.views.submit_score_view import SubmitScoreAPI
from apis.views.top_leaderboard_view import TopLeaderboardAPI
from apis.views.user_rank_view import UserRankAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'leaderboard'

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('leaderboard/submit/', SubmitScoreAPI.as_view(), name='submit-score'),
    path('leaderboard/top/', TopLeaderboardAPI.as_view(), name='top-leaderboard'),
    path('leaderboard/rank/<int:user_id>/', UserRankAPI.as_view(), name='user-rank'),
]
