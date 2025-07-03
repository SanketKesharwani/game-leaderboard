from typing import Optional
from django.core.cache import cache
from django.db.models import QuerySet
from apis.models.leaderboard import Leaderboard
from django.core.exceptions import ObjectDoesNotExist

def get_user_rank(user_id: int) -> Leaderboard:
    """
    Retrieves the leaderboard entry for a specific user.
    This function queries the database directly without any caching.
    Args:
        user_id (int): The unique identifier of the user whose rank to retrieve
    Returns:
        Leaderboard: The user's leaderboard entry containing rank and score information
    Raises:
        ValueError: If no leaderboard entry exists for the specified user
    """
    try:
        user_leaderboard_entry: Leaderboard = (
            Leaderboard.objects
            .select_related('user')
            .get(user_id=user_id)
        )
    except ObjectDoesNotExist:
        raise ValueError("Leaderboard entry does not exist for this user.")
    return user_leaderboard_entry