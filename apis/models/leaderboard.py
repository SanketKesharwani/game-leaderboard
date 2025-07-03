from django.db import models
from .user import User

class Leaderboard(models.Model):
    """
    Represents the leaderboard entry for a user, including their total score and rank.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user associated with this leaderboard entry.")
    total_score = models.IntegerField(help_text="Total score accumulated by the user.")
    rank = models.IntegerField(null=True, blank=True, help_text="Current rank of the user on the leaderboard.")

    class Meta:
        unique_together = ("user",)
        indexes = [models.Index(fields=['-total_score'])]

    def __str__(self):
        return f"#{self.rank} {self.user}: {self.total_score}"
