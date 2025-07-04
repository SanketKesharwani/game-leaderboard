from django.core.management.base import BaseCommand
from apis.models.leaderboard import Leaderboard
from django.conf import settings
import redis

class Command(BaseCommand):
    help = 'Sync leaderboard data from SQLite to Redis ZSET.'

    def handle(self, *args, **options):
        # Connect to Redis using the same settings as the app
        r = redis.Redis.from_url(settings.LEADERBOARD_ZSET_URL)
        # Clear the existing leaderboard ZSET
        r.delete('leaderboard:zset')
        # Fetch all leaderboard entries, order by total_score descending
        entries = Leaderboard.objects.select_related('user').order_by('-total_score')
        count = 0
        for entry in entries:
            # Add each user to the ZSET with their total_score
            r.zadd('leaderboard:zset', {entry.user.id: entry.total_score})
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully synced {count} leaderboard entries to Redis.')) 