class ReturnResult:
    """
    SOLUTION: Result class for return operations
    
    This class provides better error handling and result communication
    """
    
    def __init__(self, success: bool, message: str):
        self._success = success
        self._message = message
    
    @classmethod
    def success(cls, message: str) -> 'ReturnResult':
        """Create a successful return result"""
        return cls(True, message)
    
    @classmethod
    def failure(cls, message: str) -> 'ReturnResult':
        """Create a failed return result"""
        return cls(False, message)
    
    def is_success(self) -> bool:
        """Check if the operation was successful"""
        return self._success
    
    def get_message(self) -> str:
        """Get the result message"""
        return self._message
