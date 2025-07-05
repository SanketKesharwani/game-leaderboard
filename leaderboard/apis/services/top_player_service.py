from apis.models.leaderboard import Leaderboard
from apis.models.user import User
from apis.utils.redis_singleton import get_redis_client
from apis.utils.strategy import RankingStrategy, ScoreRankingStrategy
from apis.utils.adapter import RedisCacheAdapter

# Use the singleton Redis client and wrap it with the adapter
redis_client = get_redis_client()
cache_adapter = RedisCacheAdapter(redis_client)

def get_top_n_players(number_of_players: int = 10, strategy: RankingStrategy = ScoreRankingStrategy()):
    """
    Retrieve the top N players from the leaderboard using the provided ranking strategy.
    """
    return strategy.get_rankings(Leaderboard, User, cache_adapter, number_of_players=number_of_players)