from abc import ABC, abstractmethod


class RankingStrategy(ABC):
    """
    Abstract base class for ranking strategies.
    Implementations should provide a get_rankings method.
    """
    @abstractmethod
    def get_rankings(self, *args, **kwargs):
        """
        Abstract method that must be implemented by concrete ranking strategies.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            List of ranked entries based on the specific strategy implementation
        """
        pass


class ScoreRankingStrategy(RankingStrategy):
    """
    Ranks users by their total score (default behavior).
    
    This strategy:
    1. Retrieves top N users from Redis sorted set
    2. Maps user IDs to usernames from database
    3. Returns formatted leaderboard entries with ranks
    """
    def get_rankings(self, leaderboard_model, user_model, cache_adapter, number_of_players=10):
        """
        Get rankings based on total score in descending order.
        
        Args:
            leaderboard_model: Model class for leaderboard entries
            user_model: Model class for user data
            cache_adapter: Redis cache adapter instance
            number_of_players (int): Number of top players to return (default: 10)
            
        Returns:
            list: List of dictionaries containing ranked user entries with:
                - user_id (int): User's unique identifier
                - username (str): User's display name
                - total_score (int): User's cumulative score  
                - rank (int): User's position in leaderboard
        """
        # Retrieve top N users with scores from Redis sorted set
        leaderboard_entries = cache_adapter.zrevrange(
            "leaderboard:zset",
            0,
            number_of_players - 1, 
            withscores=True
        )

        # Extract user IDs and get corresponding usernames from database
        user_identifiers = [int(user_id_bytes) for user_id_bytes, _ in leaderboard_entries]
        user_mapping = user_model.objects.filter(id__in=user_identifiers).in_bulk()

        # Build formatted leaderboard results
        leaderboard_results = []
        for position, (user_id_bytes, score) in enumerate(leaderboard_entries, 1):
            user_id = int(user_id_bytes)
            username = user_mapping[user_id].username if user_id in user_mapping else "Unknown"
            
            leaderboard_results.append({
                "user_id": user_id,
                "username": username,
                "total_score": int(score),
                "rank": position
            })

        return leaderboard_results