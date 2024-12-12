from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class WebSocketStrategy(ABC):
    """Base class for implementing WebSocket connection strategies.
    
    All cryptocurrency data source strategies should inherit from this class
    and implement its abstract methods.
    """
    
    @abstractmethod
    def get_connection_params(self) -> Dict[str, Any]:
        """Return connection parameters for the WebSocket.
        
        Returns:
            Dict containing at least 'uri' for the WebSocket connection
        """
        pass

    @abstractmethod
    def format_auth_message(self) -> Dict[str, Any]:
        """Create authentication message for the WebSocket connection.
        
        Returns:
            Dict containing the authentication message format
        """
        pass

    @abstractmethod
    async def process_message(self, message: str) -> Optional[Dict[str, Any]]:
        """Process incoming WebSocket messages.
        
        Args:
            message: Raw message string from WebSocket

        Returns:
            Processed message dict or None if message should be skipped
        """
        pass

    @abstractmethod
    def get_supported_pairs(self) -> list[str]:
        """Return list of supported cryptocurrency pairs.
        
        Returns:
            List of supported trading pairs
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the strategy.
        
        Returns:
            Strategy name as string
        """
        pass