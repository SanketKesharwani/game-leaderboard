from typing import List, Dict, Any
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from apis.serializers.score_serializer import LeaderboardEntrySerializer
from apis.services.top_player_service import get_top_n_players
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apis.decorators.exception_handling import handle_api_exceptions

class TopLeaderboardAPI(APIView):
    """
    API endpoint for retrieving top leaderboard entries.
    
    This view handles fetching the top ranked players from the leaderboard:
    - No authentication required (open endpoint)
    - Returns a configurable number of top players
    - Includes rank, score and user details
    
    Attributes:
        permission_classes (list): List of permission classes allowing public access
        serializer_class (LeaderboardEntrySerializer): Serializer for leaderboard entries
    """
    permission_classes = [AllowAny]
    serializer_class = LeaderboardEntrySerializer

    @handle_api_exceptions
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Process a GET request to retrieve top leaderboard entries.

        This method:
        1. Fetches the top N players from the leaderboard service
        2. Serializes the leaderboard data
        3. Returns formatted response with player rankings
        
        Args:
            request (Request): Django REST framework request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Response: JSON response containing list of top players with:
                - user_id (int): Player's unique identifier
                - username (str): Player's display name  
                - total_score (int): Player's cumulative score
                - rank (int): Player's leaderboard position
                
        Raises:
            ValidationError: When leaderboard data cannot be retrieved
            Exception: For unexpected processing errors
        """
        # Fetch top players from service layer
        leaderboard_entries: List[Dict[str, Any]] = get_top_n_players(number_of_players=10)
        
        # Serialize leaderboard data
        serializer: LeaderboardEntrySerializer = self.serializer_class(
            leaderboard_entries, 
            many=True
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )