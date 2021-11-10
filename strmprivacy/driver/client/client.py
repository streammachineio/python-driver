from typing import Callable, Any

from .receiver import ReceiverService
from .sender import SenderService
from ..domain import ClientConfig
from ..serializer import SerializationType


class StrmPrivacyClient(object):
    def __init__(self, billing_id: str, client_id: str, client_secret: str, config: ClientConfig):
        """
        Class to interact with STRM Privacy. For each stream, a separate instance of `StrmPrivacyClient`
        is required.

        :param billing_id: unique customer identifier
        :param client_id: unique stream identifier
        :param client_secret: secret to authenticate this stream
        :param config: internal configuration (only change if instructed)
        """
        self._sender_service = SenderService(billing_id, client_id, client_secret, config)
        self._receiver_service = ReceiverService(billing_id, client_id, client_secret, config)

    async def start_timers(self):
        await self._sender_service.start_timer()
        await self._receiver_service.start_timer()

    async def send(self, event, serialization_type: SerializationType) -> str:
        return await self._sender_service.asend(event, serialization_type)

    async def start_receiving_ws(self, as_json: bool, consumer: Callable[[Any], Any]):
        return await self._receiver_service.start(as_json, consumer)

    async def close(self):
        self._receiver_service.close()
