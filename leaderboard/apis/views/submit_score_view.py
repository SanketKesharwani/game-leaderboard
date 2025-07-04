from typing import Dict, Any, Tuple
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from apis.serializers.leaderboard_serializer import ScoreSubmissionSerializer
from apis.services.submit_score_service import submit_score
from rest_framework.permissions import IsAuthenticated
from apis.decorators.exception_handling import handle_api_exceptions

class SubmitScoreAPI(generics.GenericAPIView):
    """
    API endpoint for submitting and processing game scores.
    
    This view handles the submission of game scores, including:
    - Authentication verification
    - Score data validation
    - Score processing and rank calculation
    - Response formatting with updated statistics
    
    Attributes:
        permission_classes (list): List of permission classes requiring authentication
        serializer_class (ScoreSubmissionSerializer): Serializer for score validation
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSubmissionSerializer

    @handle_api_exceptions
    def post(self, request: Request) -> Response:
        """
        Process a POST request to submit a new game score.

        This method:
        1. Validates the incoming score submission data
        2. Processes the score through the service layer
        3. Returns updated user statistics
        
        Args:
            request (Request): Django REST framework request object containing score data
            
        Returns:
            Response: JSON response containing:
                - user_id (int): ID of the user who submitted the score
                - new_total (int): Updated cumulative score for the user
                - rank (int): New leaderboard position (1-based)
                
        Raises:
            ValidationError: When submitted data fails validation
            ValueError: When referenced user does not exist
            Exception: For unexpected processing errors
        """
        # Extract and validate submission data
        submission_data: Dict[str, Any] = request.data.copy()
        serializer: ScoreSubmissionSerializer = self.get_serializer(data=submission_data)
        serializer.is_valid(raise_exception=True)

        # Process score submission through service layer
        score_results: Tuple[int, int] = submit_score(**serializer.validated_data)
        updated_total: int = score_results[0]
        new_rank: int = score_results[1]

        # Prepare response data
        response_data: Dict[str, Any] = {
            "user_id": serializer.validated_data["user_id"],
            "new_total": updated_total,
            "rank": new_rank
        }

        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED
        )