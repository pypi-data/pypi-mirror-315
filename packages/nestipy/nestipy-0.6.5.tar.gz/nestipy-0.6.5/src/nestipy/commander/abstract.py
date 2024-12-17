from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Abstract base class for CLI commands."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the command."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """The description of the command."""
        pass

    @abstractmethod
    async def run(self, context: dict):
        """The method to handle the command logic.

        Args:
            context (dict): Contains options and arguments for the command.
        """
        pass
