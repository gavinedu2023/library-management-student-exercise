from typing import Optional

from ..python_library.loan import Loan


class BorrowResult:
    """
    SOLUTION: Result class for borrow operations
    
    This class provides better error handling and result communication
    """
    
    def __init__(self, success: bool, message: str, loan: Optional[Loan] = None):
        self._success = success
        self._message = message
        self._loan = loan
    
    @classmethod
    def success(cls, loan: Loan) -> 'BorrowResult':
        """Create a successful borrow result"""
        return cls(True, "Book borrowed successfully", loan)
    
    @classmethod
    def failure(cls, message: str) -> 'BorrowResult':
        """Create a failed borrow result"""
        return cls(False, message, None)
    
    def is_success(self) -> bool:
        """Check if the operation was successful"""
        return self._success
    
    def get_message(self) -> str:
        """Get the result message"""
        return self._message
    
    def get_loan(self) -> Optional[Loan]:
        """Get the loan object if successful"""
        return self._loan
