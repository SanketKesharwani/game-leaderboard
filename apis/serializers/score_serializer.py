from rest_framework import serializers
from apis.models.leaderboard import Leaderboard

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for leaderboard entries, including username and rank.
    """
    username = serializers.CharField(source='user.username', read_only=True, help_text="Username of the leaderboard entry owner.")

    class Meta:
        model  = Leaderboard
        fields = ['user_id', 'username', 'total_score', 'rank']