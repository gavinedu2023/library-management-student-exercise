from abc import ABC, abstractmethod

from ..python_library.loan import Loan


class FineCalculationStrategy(ABC):
    """
    SOLUTION: Strategy Pattern Interface for Fine Calculation
    
    This interface allows different fine calculation algorithms to be plugged in.
    Benefits:
    1. Makes fine calculation algorithms interchangeable
    2. Easy to add new fine strategies (student discounts, member benefits)
    3. Improves testability by allowing mock implementations
    4. Follows Open/Closed Principle - open for extension, closed for modification
    """
    
    @abstractmethod
    def calculate_fine(self, loan: Loan, loan_duration_days: int) -> float:
        """Calculate the fine for a loan"""
        pass
