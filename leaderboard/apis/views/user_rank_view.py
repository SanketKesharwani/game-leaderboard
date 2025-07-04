from typing import Dict, Any
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from apis.serializers.score_serializer import LeaderboardEntrySerializer
from apis.services.ranking_service import get_user_rank
from rest_framework.permissions import IsAuthenticated
from apis.decorators.exception_handling import handle_api_exceptions

class UserRankAPI(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a user's current leaderboard ranking.
    
    This view handles fetching an authenticated user's rank information including:
    - Current leaderboard position
    - Total accumulated score
    - User profile details
    
    Attributes:
        permission_classes (list): List of permission classes requiring authentication
        serializer_class (LeaderboardEntrySerializer): Serializer for rank data
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LeaderboardEntrySerializer

    @handle_api_exceptions
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Process a GET request to retrieve a user's leaderboard ranking.

        This method:
        1. Extracts the user ID from the request
        2. Fetches the user's rank data from the service layer
        3. Serializes and returns the ranking information
        
        Args:
            request (Request): Django REST framework request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments containing user_id
            
        Returns:
            Response: JSON response containing:
                - user_id (int): User's unique identifier
                - username (str): User's display name
                - total_score (int): User's cumulative score
                - rank (int): User's current leaderboard position
                
        Raises:
            ValidationError: When rank data cannot be retrieved
            Exception: For unexpected processing errors
        """
        # Extract and validate user ID
        user_id: int = int(self.kwargs.get('user_id'))
        
        # Fetch rank data from service layer
        user_rank_data: Dict[str, Any] = get_user_rank(user_id)
        
        # Serialize rank information
        serializer: LeaderboardEntrySerializer = self.get_serializer(user_rank_data)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )