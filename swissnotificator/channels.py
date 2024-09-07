import io
import json
from datetime import datetime

from skpy import Skype, SkypeChat

from abc import ABC, abstractmethod
from typing import List, Optional


class NotificationChannel(ABC):
    """Abstract base class representing a notification channel."""

    @abstractmethod
    def send_message(self, message: str, level: str, attachments: List[io.BytesIO]):
        """Sends a message through the notification channel."""
        pass


class SkypeChannel(NotificationChannel):
    """Concrete class representing the Skype notification channel."""

    _client: Skype
    _skype_chats: List[SkypeChat]

    def __init__(self, username: str, password: str, skype_chat_ids: List[str]):
        """Constructor of the Skype channel."""
        self._client = Skype(username, password)
        if not skype_chat_ids:
            raise ValueError(
                "Can't construct Skype channel instance without channels ids."
            )
        self._skype_chats = []
        for channel_id in skype_chat_ids:
            self._skype_chats.append(self._client.chats.chat(channel_id))

    def _send_message_to_chat(
        self, skype_chat: SkypeChat, message: str, attachments: List[io.BytesIO]
    ):
        """Send message to the particular Skype chat."""
        skype_chat.sendMsg(message, rich=True)
        for attachment in attachments:
            skype_chat.sendFile(attachment, attachment.name)

    def send_message(self, message: str, level: str, attachments: List[io.BytesIO]):
        """Sends a message through the notification channel."""
        message = f"<b>{level}</b>\n{message}"
        for channel_id in self._skype_chats:
            self._send_message_to_chat(channel_id, message, attachments)
