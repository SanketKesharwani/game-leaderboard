from abc import ABC, abstractmethod

class LeaderboardCommand(ABC):
    """
    Abstract base class for leaderboard-related commands.
    Subclasses should implement the execute method.
    """
    @abstractmethod
    def execute(self):
        pass 