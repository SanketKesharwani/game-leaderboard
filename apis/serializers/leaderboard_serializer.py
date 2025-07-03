from rest_framework import serializers
from typing import Optional

class ScoreSubmissionSerializer(serializers.Serializer):
    """
    Serializer for validating and processing game score submissions.
    
    This serializer handles the validation of score submission data including:
    - User identification
    - Score value validation
    - Game mode specification
    
    Attributes:
        user_id (int): Unique identifier of the user submitting the score
        score (int): Points achieved in the game session (must be non-negative)
        game_mode (str): Identifier for the type of game played
    """
    user_id: int = serializers.IntegerField(
        required=True,
        help_text="Unique identifier of the user submitting the score"
    )
    score: int = serializers.IntegerField(
        required=True,
        min_value=0,
        help_text="Points achieved in the game session (must be non-negative)"
    )
    game_mode: str = serializers.CharField(
        required=True,
        max_length=50,
        help_text="Identifier for the type of game played"
    )