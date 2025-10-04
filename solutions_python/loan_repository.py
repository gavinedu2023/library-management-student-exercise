from abc import ABC, abstractmethod
from typing import List, Optional

from ..python_library.loan import Loan


class LoanRepository(ABC):
    """
    SOLUTION: Repository Pattern Interface for Loans
    """
    
    @abstractmethod
    def save(self, loan: Loan) -> None:
        """Save a loan to the repository"""
        pass
    
    @abstractmethod
    def find_by_id(self, loan_id: str) -> Optional[Loan]:
        """Find a loan by its ID"""
        pass
    
    @abstractmethod
    def update(self, loan: Loan) -> None:
        """Update an existing loan in the repository"""
        pass
    
    @abstractmethod
    def delete(self, loan_id: str) -> None:
        """Delete a loan from the repository"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Loan]:
        """Get all loans from the repository"""
        pass
    
    @abstractmethod
    def find_by_member_id(self, member_id: str) -> List[Loan]:
        """Find all loans for a specific member"""
        pass
