# Library Management System - Solutions Package
# This package contains improved implementations with design patterns and best practices

from .book_repository import BookRepository
from .borrow_result import BorrowResult
from .fine_calculation_strategy import FineCalculationStrategy
from .improved_library_service import ImprovedLibraryService
from .loan_repository import LoanRepository
from .member_repository import MemberRepository
from .return_result import ReturnResult
from .standard_fine_strategy import StandardFineStrategy
from .student_fine_strategy import StudentFineStrategy

__all__ = [
    'BookRepository',
    'BorrowResult', 
    'FineCalculationStrategy',
    'ImprovedLibraryService',
    'LoanRepository',
    'MemberRepository',
    'ReturnResult',
    'StandardFineStrategy',
    'StudentFineStrategy'
]
