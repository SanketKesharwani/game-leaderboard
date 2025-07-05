from django.core.management.base import BaseCommand
from apis.utils.command import LeaderboardCommand
from django.conf import settings
import redis
from apis.utils.redis_singleton import get_redis_client

class SyncLeaderboardToRedisCommand(LeaderboardCommand):
    def execute(self):
        r = get_redis_client()
        r.delete('leaderboard:zset')
        from apis.models.leaderboard import Leaderboard
        entries = Leaderboard.objects.select_related('user').order_by('-total_score')
        count = 0
        for entry in entries:
            r.zadd('leaderboard:zset', {entry.user.id: entry.total_score})
            count += 1
        return count

class Command(BaseCommand):
    help = 'Sync leaderboard data from SQLite to Redis ZSET.'

    def handle(self, *args, **options):
        sync_command = SyncLeaderboardToRedisCommand()
        count = sync_command.execute()
        self.stdout.write(self.style.SUCCESS(f'Successfully synced {count} leaderboard entries to Redis.')) 