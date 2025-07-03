from typing import Tuple, Optional
from django.db import transaction
from django.db.models import F
from apis.models.game_session import GameSession
from apis.models.leaderboard import Leaderboard
from apis.models.user import User
from django.core.exceptions import ObjectDoesNotExist
import redis
from django.conf import settings

# Initialize Redis client for leaderboard sorted set storage
redis_client: redis.Redis = redis.Redis.from_url(settings.LEADERBOARD_ZSET_URL)

def submit_score(user_id: int, score: int, game_mode: str) -> Tuple[int, int]:
    """
    Submit a game score and update the user's leaderboard ranking.

    This function handles the complete score submission process:
    1. Records the game session in the database
    2. Updates the user's cumulative score
    3. Recalculates and updates the user's leaderboard rank
    4. Synchronizes the data with Redis cache

    Args:
        user_id (int): Unique identifier of the user submitting the score
        score (int): Points achieved in the game session
        game_mode (str): Identifier for the type of game played

    Returns:
        Tuple[int, int]: A tuple containing:
            - total_score (int): User's updated cumulative score
            - new_rank (int): User's new position on the leaderboard (1-based)

    Raises:
        ValueError: If no user exists with the provided user_id
    """
    with transaction.atomic():
        try:
            # Acquire row-level lock on user record for atomic updates
            current_user: User = User.objects.select_for_update().get(pk=user_id)
        except ObjectDoesNotExist:
            raise ValueError(f"User with ID {user_id} does not exist")

        # Record the game session details
        game_session: GameSession = GameSession.objects.create(
            user=current_user,
            score=score,
            game_mode=game_mode
        )

        # Update or create leaderboard entry with atomic score increment
        leaderboard_entry: Leaderboard
        created: bool
        leaderboard_entry, created = Leaderboard.objects.select_for_update().get_or_create(
            user=current_user,
            defaults={'total_score': score}
        )
        
        if not created:
            leaderboard_entry.total_score = F('total_score') + score
            leaderboard_entry.save(update_fields=['total_score'])
            leaderboard_entry.refresh_from_db(fields=['total_score'])

        # Calculate new leaderboard position
        current_rank: int = Leaderboard.objects.filter(
            total_score__gt=leaderboard_entry.total_score
        ).count() + 1
        
        leaderboard_entry.rank = current_rank
        leaderboard_entry.save(update_fields=['rank'])

    # Update Redis sorted set with new total score
    redis_client.zadd("leaderboard:zset", {user_id: int(leaderboard_entry.total_score)})

    # Retrieve final score and rank from Redis
    final_score: Optional[float] = redis_client.zscore("leaderboard:zset", user_id)
    final_rank: Optional[int] = redis_client.zrevrank("leaderboard:zset", user_id)

    return (
        int(final_score if final_score is not None else 0),
        (final_rank + 1) if final_rank is not None else 1
    )