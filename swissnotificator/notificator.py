import io
import logging
from typing import List
from .channels import NotificationChannel, SkypeChannel


logger = logging.getLogger(__name__)


class Notificator:
    """Class for sending messages to different notification channels."""

    _channels: List[NotificationChannel]

    def __init__(self, channels: List[NotificationChannel]):
        """Initializes a Notificator instance.

        Args:
            channels (list): A list of NotificationChannel instances.
        """
        if not channels:
            raise ValueError("Can't construct notificator instance without channels.")
        self._channels = channels

    def init_app(self, app):
        """Initialize from flask application."""
        if app.config["SKYPE_NOTIFICATION_CHANNELS"]:
            self._channels.append(
                SkypeChannel(
                    app.config["SKYPE_LOGIN"],
                    app.config["SKYPE_PASSWORD"],
                    app.config["SKYPE_NOTIFICATION_CHANNELS"],
                )
            )

    def is_active(self):
        """Return true if there is any channels to send notification to."""
        return bool(self._channels)

    def notify(self, message: str, level: str, attachments: List[io.BytesIO] = ()):
        """Send notification.

         Args:
            message (str): The message text to be sent.
            level (int): The log level of the message.
            attachments  (List[io.BytesIO]): list of file attachments

        The log level will be included in the message if a prefix is set.
        """
        # if kwargs:
        #     print(kwargs)
        #     file_obj = io.BytesIO(json.dumps(kwargs).encode())
        #     file_obj.name = f"{datetime.utcnow().isoformat()}.json"
        for chanel in self._channels:
            try:
                chanel.send_message(message, level, attachments)
            except Exception as e:
                logger.error(
                    f"Failed to send the notification using {chanel}: {e}",
                    extra={"is_notificator_message": True},
                )
