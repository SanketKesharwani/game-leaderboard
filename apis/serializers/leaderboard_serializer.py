from rest_framework import serializers

class ScoreSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting a score. Validates user, score, and game mode.
    """
    user_id = serializers.IntegerField(required=True)
    score = serializers.IntegerField(min_value=0, required=True)
    game_mode = serializers.CharField(max_length=50, required=True)