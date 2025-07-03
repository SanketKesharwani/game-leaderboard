from django.contrib import admin
from .models.user import User
from .models.game_session import GameSession
from .models.leaderboard import Leaderboard

admin.site.register(User)
admin.site.register(GameSession)
admin.site.register(Leaderboard)
