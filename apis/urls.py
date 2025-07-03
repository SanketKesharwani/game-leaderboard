from django.urls import path
from apis.views.submit_score_view import SubmitScoreAPI
from apis.views.top_leaderboard_view import TopLeaderboardAPI
from apis.views.user_rank_view import UserRankAPI

app_name = 'leaderboard'

urlpatterns = [
    path('leaderboard/submit/', SubmitScoreAPI.as_view(), name='submit-score'),
    path('leaderboard/top/', TopLeaderboardAPI.as_view(), name='top-leaderboard'),
    path('leaderboard/rank/', UserRankAPI.as_view(), name='user-rank'),
]
