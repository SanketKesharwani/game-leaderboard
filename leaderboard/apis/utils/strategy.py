from abc import ABC, abstractmethod

class RankingStrategy(ABC):
    """
    Abstract base class for ranking strategies.
    Implementations should provide a get_rankings method.
    """
    @abstractmethod
    def get_rankings(self, *args, **kwargs):
        pass

class ScoreRankingStrategy(RankingStrategy):
    """
    Ranks users by their total score (default behavior).
    """
    def get_rankings(self, leaderboard_model, user_model, cache_adapter, number_of_players=10):
        # Use cache adapter for score-based ranking
        leaderboard_entries = cache_adapter.zrevrange(
            "leaderboard:zset",
            0,
            number_of_players - 1,
            withscores=True
        )
        user_identifiers = [int(user_id_bytes) for user_id_bytes, _ in leaderboard_entries]
        user_mapping = user_model.objects.filter(id__in=user_identifiers).in_bulk()
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

class GamesPlayedRankingStrategy(RankingStrategy):
    """
    Ranks users by the number of games played
    """
    def get_rankings(self, leaderboard_model, user_model, cache_adapter, number_of_players=10):
        # Example: Query DB for games played count
        from apis.models.game_session import GameSession
        from django.db.models import Count
        games_played = GameSession.objects.values('user_id').annotate(
            games_played=Count('id')
        ).order_by('-games_played')[:number_of_players]
        user_mapping = user_model.objects.filter(id__in=[g['user_id'] for g in games_played]).in_bulk()
        leaderboard_results = []
        for position, entry in enumerate(games_played, 1):
            user_id = entry['user_id']
            username = user_mapping[user_id].username if user_id in user_mapping else "Unknown"
            leaderboard_results.append({
                "user_id": user_id,
                "username": username,
                "games_played": entry['games_played'],
                "rank": position
            })
        return leaderboard_results 