from typing import List, Dict, Union, Tuple, Optional
from apis.models.user import User
import redis
from django.conf import settings

# Initialize Redis client for leaderboard sorted set storage
redis_client: redis.Redis = redis.Redis.from_url(settings.LEADERBOARD_ZSET_URL)

def get_top_n_players(number_of_players: int = 10) -> List[Dict[str, Union[int, str]]]:
    """
    Retrieve the top N players from the leaderboard stored in Redis sorted set.
    
    This function fetches the highest scoring players, including:
    1. Their user ID and username
    2. Total accumulated score
    3. Current leaderboard rank (1-based)

    Args:
        number_of_players (int): Number of top players to retrieve. Defaults to 10.

    Returns:
        List[Dict[str, Union[int, str]]]: List of dictionaries containing:
            - user_id (int): Unique identifier of the user
            - username (str): Display name of the user
            - total_score (int): User's cumulative score
            - rank (int): User's position on the leaderboard (1-based)
    """
    # Fetch top N entries from Redis sorted set with scores
    leaderboard_entries: List[Tuple[bytes, float]] = redis_client.zrevrange(
        "leaderboard:zset",
        0,
        number_of_players - 1,
        withscores=True
    )

    # Extract user IDs from Redis entries
    user_identifiers: List[int] = [
        int(user_id_bytes) for user_id_bytes, _ in leaderboard_entries
    ]

    # Bulk fetch user objects from database
    user_mapping: Dict[int, User] = User.objects.filter(
        id__in=user_identifiers
    ).in_bulk()

    # Construct leaderboard response
    leaderboard_results: List[Dict[str, Union[int, str]]] = []
    
    for position, (user_id_bytes, score) in enumerate(leaderboard_entries, 1):
        user_id: int = int(user_id_bytes)
        username: str = user_mapping[user_id].username if user_id in user_mapping else "Unknown"
        
        leaderboard_results.append({
            "user_id": user_id,
            "username": username,
            "total_score": int(score),
            "rank": position
        })

    return leaderboard_results