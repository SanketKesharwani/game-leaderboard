from typing import Dict, Any
from rest_framework import status, generics
from rest_framework.request import Request 
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from apis.serializers.leaderboard_serializer import ScoreSubmissionSerializer
from apis.services.submit_score_service import submit_score

class SubmitScoreAPI(generics.GenericAPIView):
    """
    API endpoint for submitting a user's game score.
    
    This endpoint requires user authentication and follows the Single Responsibility Principle
    by delegating all business logic to the service layer. It validates the incoming score
    submission data and returns the updated total score and rank.
    """
    serializer_class = ScoreSubmissionSerializer

    def post(self, request: Request) -> Response:
        """
        Handle POST request to submit a new game score.
        
        Args:
            request (Request): The incoming HTTP request containing score data
            
        Returns:
            Response: JSON response with updated total score and rank
            
        Raises:
            ValidationError: If the submitted data is invalid
            ValueError: If the user does not exist
        """
        try:
            submission_data: Dict[str, Any] = request.data.copy()
            submission_data['user_id'] = request.user.id
            
            serializer: ScoreSubmissionSerializer = self.get_serializer(data=submission_data)
            serializer.is_valid(raise_exception=True)
            
            updated_total, new_rank = submit_score(**serializer.validated_data)
            
            response_data: Dict[str, Any] = {
                "user_id": request.user.id,
                "new_total": updated_total,
                "rank": new_rank
            }
            
            return Response(
                data=response_data,
                status=status.HTTP_201_CREATED
            )
            
        except ValidationError as e:
            return Response(
                data={"error": "Invalid submission data", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                data={"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )