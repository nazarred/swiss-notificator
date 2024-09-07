import logging
from swissnotificator import Notificator


class NotificatorHandler(logging.Handler):
    """Custom logging handler that sends log messages to a Notificator instance."""

    def __init__(self, notificator: Notificator):
        """Initialize the handler with a Notificator instance."""
        super().__init__()
        self.notificator = notificator

    def emit(self, record):
        """Send a log message to the Notificator instance."""
        # Skip messages from the Notificator itself
        if getattr(record, "is_notificator_message", False):
            return
        log_entry = self.format(record)
        self.notificator.notify(
            log_entry,
            level=record.levelname,
            attachments=getattr(record, "attachments", []),
        )
