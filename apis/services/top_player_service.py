from typing import List, Optional
from django.db.models import QuerySet
from apis.models.leaderboard import Leaderboard


def get_top_n(num_players: int = 10) -> List[Leaderboard]:
    """
    Retrieves the top N leaderboard entries directly from the database without caching.
    Args:
        num_players (int): Number of top players to retrieve. Defaults to 10.
    Returns:
        List[Leaderboard]: List of top N leaderboard entries, ordered by rank ascending.
        Each entry contains the player's rank, total score, and related user data.
    """
    leaderboard_query: QuerySet[Leaderboard] = (
        Leaderboard.objects
        .select_related('user')
        .order_by('-total_score')[:num_players]
    )
    leaderboard_results: List[Leaderboard] = list(leaderboard_query)
    return leaderboard_results