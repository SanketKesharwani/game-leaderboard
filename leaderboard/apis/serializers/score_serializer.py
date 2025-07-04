from rest_framework import serializers
from typing import Optional

class LeaderboardEntrySerializer(serializers.Serializer):
    """
    Serializer for leaderboard entries containing user ranking information.
    
    This serializer handles dictionary input from Redis-backed storage and includes:
    - User identification (ID and username)
    - Score and ranking information
    
    Attributes:
        user_id (int): Unique identifier for the user
        username (str): Display name of the user
        total_score (int): Cumulative score achieved by the user
        rank (Optional[int]): Current position on the leaderboard (1-based, nullable)
    """
    user_id: int = serializers.IntegerField(
        help_text="Unique identifier of the user"
    )
    username: str = serializers.CharField(
        help_text="Display name of the user"
    )
    total_score: int = serializers.IntegerField(
        help_text="User's cumulative score across all games"
    )
    rank: Optional[int] = serializers.IntegerField(
        allow_null=True,
        help_text="User's current position on the leaderboard (1-based)"
    )