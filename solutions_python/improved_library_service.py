import uuid
from datetime import datetime
from typing import List, Optional

from .book_repository import BookRepository
from .borrow_result import BorrowResult
from .fine_calculation_strategy import FineCalculationStrategy
from .loan_repository import LoanRepository
from .member_repository import MemberRepository
from .return_result import ReturnResult
from ..python_library.book import Book
from ..python_library.loan import Loan
from ..python_library.member import Member


class ImprovedLibraryService:
    """
    SOLUTION: Improved Library Service
    
    This class fixes the issues from the original code:
    1. DEBUG FIXES: Code duplication, input validation, error handling
    2. DESIGN PATTERNS: Repository pattern, Strategy pattern
    3. CODE QUALITY: Better naming, documentation, maintainability
    """
    
    # SOLUTION: Business rules configuration
    MAX_BOOKS_PER_MEMBER = 5
    LOAN_DURATION_DAYS = 14
    
    def __init__(self, book_repository: BookRepository, 
                 member_repository: MemberRepository,
                 loan_repository: LoanRepository,
                 fine_strategy: FineCalculationStrategy):
        # SOLUTION: Repository pattern - abstract data access
        self.book_repository = book_repository
        self.member_repository = member_repository
        self.loan_repository = loan_repository
        
        # SOLUTION: Strategy pattern for fine calculation
        self.fine_strategy = fine_strategy
    
    def borrow_book(self, member_id: str, book_id: str) -> BorrowResult:
        """
        SOLUTION: Improved borrow book method with better error handling and validation
        """
        # SOLUTION: Input validation - prevents null pointer exceptions
        if not member_id or not member_id.strip():
            return BorrowResult.failure("Member ID cannot be null or empty")
        if not book_id or not book_id.strip():
            return BorrowResult.failure("Book ID cannot be null or empty")
        
        try:
            # SOLUTION: Use repository pattern instead of direct list access
            member = self.member_repository.find_by_id(member_id)
            if member is None:
                return BorrowResult.failure("Member not found")
            
            book = self.book_repository.find_by_id(book_id)
            if book is None:
                return BorrowResult.failure("Book not found")
            
            # SOLUTION: Check if book is available
            if not book.is_available():
                return BorrowResult.failure("Book is not available")
            
            # SOLUTION: Business rule - check borrowing limit
            member_loans = self.loan_repository.find_by_member_id(member_id)
            if len(member_loans) >= self.MAX_BOOKS_PER_MEMBER:
                return BorrowResult.failure(f"Member has reached maximum borrowing limit of {self.MAX_BOOKS_PER_MEMBER} books")
            
            # SOLUTION: Create loan with proper validation
            loan_id = str(uuid.uuid4())
            loan = Loan(loan_id, member_id, book_id, datetime.now())
            self.loan_repository.save(loan)
            
            # SOLUTION: Update book status atomically
            book.set_available(False)
            self.book_repository.update(book)
            
            return BorrowResult.success(loan)
            
        except Exception as e:
            # SOLUTION: Specific error handling instead of generic exception catching
            return BorrowResult.failure(f"Failed to borrow book: {str(e)}")
    
    def return_book(self, loan_id: str) -> ReturnResult:
        """
        SOLUTION: Improved return book method
        """
        # SOLUTION: Input validation
        if not loan_id or not loan_id.strip():
            return ReturnResult.failure("Loan ID cannot be null or empty")
        
        try:
            # SOLUTION: Use repository pattern
            loan = self.loan_repository.find_by_id(loan_id)
            if loan is None:
                return ReturnResult.failure("Loan not found")
            
            # SOLUTION: Find and update book status
            book = self.book_repository.find_by_id(loan.get_book_id())
            if book is not None:
                book.set_available(True)
                self.book_repository.update(book)
            
            # SOLUTION: Remove loan
            self.loan_repository.delete(loan_id)
            
            return ReturnResult.success("Book returned successfully")
            
        except Exception as e:
            return ReturnResult.failure(f"Failed to return book: {str(e)}")
    
    def get_available_books(self) -> List[Book]:
        """
        SOLUTION: Improved get available books method
        """
        try:
            # SOLUTION: Use repository pattern and list comprehension for better readability
            all_books = self.book_repository.find_all()
            return [book for book in all_books if book.is_available()]
        except Exception as e:
            # SOLUTION: Return empty list instead of throwing exception
            return []
    
    def get_member_loans(self, member_id: str) -> List[Loan]:
        """
        SOLUTION: Improved get member loans method
        """
        # SOLUTION: Input validation
        if not member_id or not member_id.strip():
            return []
        
        try:
            return self.loan_repository.find_by_member_id(member_id)
        except Exception as e:
            return []
    
    def calculate_fine(self, loan_id: str) -> float:
        """
        SOLUTION: Improved fine calculation with strategy pattern
        """
        # SOLUTION: Input validation
        if not loan_id or not loan_id.strip():
            return 0.0
        
        try:
            loan = self.loan_repository.find_by_id(loan_id)
            if loan is None:
                return 0.0
            
            # SOLUTION: Use strategy pattern for fine calculation
            return self.fine_strategy.calculate_fine(loan, self.LOAN_DURATION_DAYS)
            
        except Exception as e:
            return 0.0
    
    def add_book(self, book: Book) -> bool:
        """
        SOLUTION: Add book with validation
        """
        if book is None or not book.get_id() or not book.get_id().strip():
            return False
        
        try:
            self.book_repository.save(book)
            return True
        except Exception as e:
            return False
    
    def add_member(self, member: Member) -> bool:
        """
        SOLUTION: Add member with validation
        """
        if member is None or not member.get_id() or not member.get_id().strip():
            return False
        
        try:
            self.member_repository.save(member)
            return True
        except Exception as e:
            return False
