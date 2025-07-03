from typing import List
from rest_framework import generics
from django.core.exceptions import ValidationError
from apis.serializers.score_serializer import LeaderboardEntrySerializer
from apis.services.top_player_service import get_top_n
from apis.models.leaderboard import Leaderboard

class TopLeaderboardAPI(generics.ListAPIView):
    """
    API endpoint to retrieve the top N leaderboard entries.
    
    This endpoint is open to all users and returns the top ranked players.
    Uses caching for performance optimization and includes rate limiting 
    for abuse prevention.
    
    Returns:
        List[Leaderboard]: A list of the top N leaderboard entries, ordered by rank
        
    Raises:
        ValidationError: If there is an error retrieving the leaderboard data
        Exception: For any unexpected errors during processing
    """
    serializer_class = LeaderboardEntrySerializer

    def get_queryset(self) -> List[Leaderboard]:
        """
        Retrieve the top 10 leaderboard entries.
        
        Returns:
            List[Leaderboard]: The top 10 leaderboard entries
            
        Raises:
            ValidationError: If there is an error retrieving the data
        """
        try:
            return get_top_n(10)
        except ValidationError as e:
            raise ValidationError(f"Failed to retrieve leaderboard: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error retrieving leaderboard: {str(e)}")