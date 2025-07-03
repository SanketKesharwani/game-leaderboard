from rest_framework import serializers
from apis.models.game_session import GameSession

class ScoreSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting a score. Validates user, score, and game mode.
    """
    class Meta:
        model = GameSession
        fields = ['user_id', 'score', 'game_mode']