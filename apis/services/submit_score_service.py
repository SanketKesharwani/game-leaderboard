from django.db import transaction
from django.db.models import F
from typing import Tuple
from apis.models.game_session import GameSession
from apis.models.leaderboard import Leaderboard
from apis.models.user import User
from django.core.exceptions import ObjectDoesNotExist


def submit_score(user_id: int, score: int, game_mode: str) -> Tuple[int, int]:
    """
    Handles the business logic for submitting a score:
    - Records the game session
    - Updates the user's total score 
    - Recomputes and updates the user's rank
    - Uses transactions for data integrity

    Args:
        user_id (int): The ID of the user submitting the score
        score (int): The score achieved in the game
        game_mode (str): The mode of the game played

    Returns:
        Tuple[int, int]: A tuple containing (total_score, new_rank)

    Raises:
        ValueError: If the user does not exist
    """
    # Use transaction to ensure data consistency across operations
    with transaction.atomic():
        try:
            # Lock the user record to prevent concurrent updates
            player = User.objects.select_for_update().get(pk=user_id)
        except ObjectDoesNotExist:
            raise ValueError("User does not exist.")
        
        # Create new game session record with the submitted score
        _ = GameSession.objects.create(
            user=player, 
            score=score, 
            game_mode=game_mode
        )
        
        # Update or create user's leaderboard entry with new score
        leaderboard_entry, _ = Leaderboard.objects.select_for_update().get_or_create(user=player)
        leaderboard_entry.total_score = F('total_score') + score  # Use F() to prevent race conditions
        leaderboard_entry.save(update_fields=['total_score'])
        
        # Refresh the instance to get the actual updated score
        leaderboard_entry.refresh_from_db(fields=['total_score'])
        
        # Calculate new rank based on number of players with higher scores
        # This query leverages the index on -total_score for efficiency
        new_rank = Leaderboard.objects.filter(
            total_score__gt=leaderboard_entry.total_score
        ).count() + 1
        leaderboard_entry.rank = new_rank
        leaderboard_entry.save(update_fields=['rank'])
        
    return leaderboard_entry.total_score, leaderboard_entry.rank