"""Socket.IO streaming functionality."""

from loguru import logger
from socketio import AsyncServer

class SocketIOManager:
    """Manages Socket.IO streaming operations."""

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the singleton instance."""
        self.sio: AsyncServer | None = None
        self.active_connections: set[str] = set()

    def set_server(self, sio: AsyncServer):
        """Set the Socket.IO server instance."""
        self.sio = sio

    async def emit_stream(self, data: dict) -> None:
        """Emit stream data to all connected clients."""
        if self.sio:
            try:
                await self.sio.emit('stream', data)
                if data.get('content'):
                    logger.debug(f"Stream data sent: {str(data.get('content'))[:50]}...")
            except Exception as e:
                logger.error(f"Error sending stream: {e}")
        else:
            logger.warning("Socket.IO server not initialized")

    async def close_stream(self) -> None:
        """Send stream close signal to all clients."""
        message = {"type": "close", "content": None}
        if self.sio:
            try:
                await self.sio.emit('stream', message)
                logger.debug("Stream close signal sent")
            except Exception as e:
                logger.error(f"Error sending close: {e}")
        else:
            logger.warning("Socket.IO server not initialized")
