from datetime import datetime, timedelta

from .fine_calculation_strategy import FineCalculationStrategy
from ..python_library.loan import Loan


class StandardFineStrategy(FineCalculationStrategy):
    """
    SOLUTION: Standard Fine Calculation Strategy
    
    This implements the standard fine calculation logic:
    - No fine for books returned within the loan period
    - $0.50 per day for books returned after the loan period
    """
    
    DAILY_FINE_RATE = 0.50
    
    def calculate_fine(self, loan: Loan, loan_duration_days: int) -> float:
        """Calculate fine using standard rates"""
        if loan is None or loan.get_borrow_date() is None:
            return 0.0
        
        # Calculate days overdue
        days_overdue = self._calculate_days_overdue(loan.get_borrow_date(), loan_duration_days)
        
        if days_overdue > 0:
            return days_overdue * self.DAILY_FINE_RATE
        
        return 0.0
    
    def _calculate_days_overdue(self, borrow_date: datetime, loan_duration_days: int) -> int:
        """Calculate the number of days a loan is overdue"""
        current_time = datetime.now()
        loan_duration = timedelta(days=loan_duration_days)
        due_date = borrow_date + loan_duration
        
        if current_time > due_date:
            overdue_days = (current_time - due_date).days
            return max(0, overdue_days)
        
        return 0
