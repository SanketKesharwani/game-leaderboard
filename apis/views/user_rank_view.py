from typing import Any
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from apis.serializers.score_serializer import LeaderboardEntrySerializer
from apis.services.ranking_service import get_user_rank
from apis.models.leaderboard import Leaderboard
from rest_framework.permissions import IsAuthenticated

class UserRankAPI(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the authenticated user's leaderboard rank.
    
    This endpoint requires user authentication and implements rate limiting to prevent abuse.
    Returns the user's current rank, total score, and related leaderboard information.
    
    Returns:
        Leaderboard: Object containing user's rank and score details
        
    Raises:
        ValidationError: If there is an error retrieving the rank data
        Exception: For any unexpected errors during processing
    """
    permission_classes = [IsAuthenticated]
    serializer_class: type[LeaderboardEntrySerializer] = LeaderboardEntrySerializer

    def get_object(self) -> Leaderboard:
        """
        Retrieves the specified user's rank information based on user_id from the URL.
        
        Returns:
            Leaderboard: Object containing user's rank and score details
            
        Raises:
            ValidationError: If there is an error retrieving the rank data
            Exception: For any unexpected errors
        """
        try:
            user_id: int = int(self.kwargs.get('user_id'))
            user_rank_data: Leaderboard = get_user_rank(user_id)
            return user_rank_data
            
        except ValidationError as e:
            raise ValidationError(f"Failed to retrieve user rank: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error retrieving user rank: {str(e)}")