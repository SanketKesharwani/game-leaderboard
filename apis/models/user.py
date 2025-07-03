from django.db import models

class User(models.Model):
    """
    Represents a user in the leaderboard system.
    """
    username = models.CharField(max_length=255, unique=True, help_text="Unique username for the user.")
    join_date = models.DateTimeField(auto_now_add=True, help_text="The date and time when the user joined.")

    class Meta:
        indexes = [models.Index(fields=['username'])]

    def __str__(self):
        return self.username
