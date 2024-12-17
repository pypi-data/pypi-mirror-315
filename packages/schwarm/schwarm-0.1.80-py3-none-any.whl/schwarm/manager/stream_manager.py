"""Manages streaming of LLM outputs using Socket.IO."""

from enum import Enum

from loguru import logger

from schwarm.telemetry.socketio_manager import SocketIOManager


class MessageType(Enum):
    """Types of messages that can be streamed."""

    DEFAULT = "default"
    TOOL = "tool"


class StreamManager:
    """Manages streaming of LLM outputs using Socket.IO.

    This implementation provides:
    - Real-time bi-directional communication
    - Support for multiple concurrent clients
    - Proper resource cleanup
    - Memory efficient streaming
    - Room-based message broadcasting
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the singleton instance."""
        self.socketio_manager = SocketIOManager()
        logger.debug("StreamManager initialized")

    async def connect(self, sid: str):
        """Handle new Socket.IO connection."""
        self.socketio_manager.active_connections.add(sid)
        logger.debug(f"New Socket.IO connection established. Total connections: {len(self.socketio_manager.active_connections)}")

    async def disconnect(self, sid: str):
        """Handle Socket.IO disconnection."""
        if sid in self.socketio_manager.active_connections:
            self.socketio_manager.active_connections.remove(sid)
        logger.debug(f"Socket.IO connection closed. Remaining connections: {len(self.socketio_manager.active_connections)}")

    async def handle_stream(self, sid: str, data: dict):
        """Handle incoming stream data from clients."""
        try:
            message_type = data.get('type', MessageType.DEFAULT.value)
            content = data.get('content')
            agent_name = data.get('agent', '')
            
            if content:
                await self.write(content, agent_name, MessageType(message_type))
        except Exception as e:
            logger.error(f"Error handling stream data: {e}")
            raise

    async def write(self, chunk: str, agent_name: str, message_type: MessageType = MessageType.DEFAULT) -> None:
        """Write a chunk to all connected Socket.IO clients.

        Args:
            chunk: Text chunk to stream
            agent_name: Name of the agent sending the message
            message_type: Type of message (default or tool output)
        """
        if not chunk:  # Avoid empty chunks
            return

        # pm = ProviderManager._instance
        # if pm and not pm.is_streaming:
        #     pm.chunk = ""
        #     pm.is_streaming = True
        # if pm:
        #     pm.chunk += chunk

        message = {
            "type": message_type.value,
            "content": chunk,
            "agent": agent_name
        }

        await self.socketio_manager.emit_stream(message)

    async def close(self) -> None:
        """Signal the end of the stream to all clients."""
        await self.socketio_manager.close_stream()


class StreamToolManager(StreamManager):
    """Tool-specific streaming manager.

    Uses the Socket.IO-based StreamManager with the TOOL message type.
    """

    async def write(self, chunk: str, agent_name: str) -> None:
        """Write a tool output chunk to the stream."""
        await super().write(chunk, agent_name, MessageType.TOOL)
