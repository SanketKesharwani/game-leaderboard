from typing import Dict, Union, Optional
from apis.models.user import User
from apis.utils.redis_singleton import get_redis_client
from apis.utils.adapter import RedisCacheAdapter

# Use the singleton Redis client
redis_client = get_redis_client()
cache_adapter = RedisCacheAdapter(redis_client)

def get_user_rank(user_id: int) -> Dict[str, Union[int, str, None]]:
    """
    Retrieve a user's leaderboard entry including their rank and score.
    
    Args:
        user_id (int): The unique identifier of the user
        
    Returns:
        Dict[str, Union[int, str, None]]: A dictionary containing:
            - user_id (int): The user's ID
            - username (str): The user's display name
            - total_score (int): The user's cumulative score
            - rank (Optional[int]): The user's current rank (1-based) or None if unranked
            
    Raises:
        ValueError: If no user exists with the provided user_id
    """
    # Get user's score from Redis leaderboard
    user_score: Optional[float] = cache_adapter.zscore("leaderboard:zset", user_id)
    
    # Fetch username, raising ValueError if user doesn't exist
    try:
        user_name: str = User.objects.get(pk=user_id).username
    except User.DoesNotExist:
        raise ValueError(f"User with id {user_id} does not exist")

    # Handle case where user has no score yet
    if user_score is None:
        return {
            "user_id": user_id,
            "username": user_name,
            "total_score": 0,
            "rank": None,
        }
    
    # Get user's rank (0-based index)
    user_rank: Optional[int] = cache_adapter.zrevrank("leaderboard:zset", user_id)
    
    return {
        "user_id": user_id,
        "username": user_name,
        "total_score": int(user_score),
        "rank": (user_rank + 1) if user_rank is not None else None,
    }