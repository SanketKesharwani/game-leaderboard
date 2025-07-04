from django.db import models
from .user import User

class GameSession(models.Model):
    """
    Represents a single game session played by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who played the session.")
    score = models.IntegerField(help_text="Score achieved in the session.")
    game_mode = models.CharField(max_length=50, help_text="Game mode for the session.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the session was played.")

    class Meta:
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', 'timestamp'])
        ]

    def __str__(self):
        return f"{self.user} – {self.score} ({self.game_mode})"
