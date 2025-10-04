import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from .book_repository import BookRepository
from .borrow_result import BorrowResult
from .fine_calculation_strategy import FineCalculationStrategy
from .improved_library_service import ImprovedLibraryService
from .loan_repository import LoanRepository
from .member_repository import MemberRepository
from .return_result import ReturnResult
from ..python_library.book import Book
from ..python_library.loan import Loan
from ..python_library.member import Member


class ComprehensiveLibraryServiceTest(unittest.TestCase):
    """
    SOLUTION: Comprehensive Test Suite
    
    This test file addresses the original code's lack of test coverage by providing:
    1. DEBUG TESTS: Tests for all the bugs found in the original code
    2. INTEGRATION TESTS: End-to-end borrowing and returning flow
    3. EDGE CASE TESTS: Boundary conditions and error scenarios
    4. BUSINESS LOGIC TESTS: Borrowing limits and business rules
    """
    
    def setUp(self):
        # Create mock repositories
        self.mock_book_repository = Mock(spec=BookRepository)
        self.mock_member_repository = Mock(spec=MemberRepository)
        self.mock_loan_repository = Mock(spec=LoanRepository)
        self.mock_fine_strategy = Mock(spec=FineCalculationStrategy)
        
        # Create service with mocked dependencies
        self.service = ImprovedLibraryService(
            self.mock_book_repository, self.mock_member_repository,
            self.mock_loan_repository, self.mock_fine_strategy
        )
        
        # Setup test data
        self.test_book = Book("book1", "Java Programming", "Author Name")
        self.test_member = Member("member1", "John Doe", "john@example.com")
    
    # SOLUTION: Unit Tests - Individual Method Testing
    # These tests verify that each method works correctly in isolation
    
    def test_borrow_book_success(self):
        """SOLUTION: Test successful borrowing scenario"""
        # This verifies the happy path works correctly
        self.mock_member_repository.find_by_id.return_value = self.test_member
        self.mock_book_repository.find_by_id.return_value = self.test_book
        self.mock_loan_repository.find_by_member_id.return_value = []
        
        result = self.service.borrow_book("member1", "book1")
        
        self.assertTrue(result.is_success())
        self.assertIsNotNone(result.get_loan())
        self.mock_loan_repository.save.assert_called_once()
        self.mock_book_repository.update.assert_called_once_with(self.test_book)
    
    def test_borrow_book_member_not_found(self):
        """SOLUTION: Test input validation - member not found"""
        # This tests the validation fix from the original code
        self.mock_member_repository.find_by_id.return_value = None
        
        result = self.service.borrow_book("invalid", "book1")
        
        self.assertFalse(result.is_success())
        self.assertEqual("Member not found", result.get_message())
    
    def test_borrow_book_book_not_found(self):
        """SOLUTION: Test input validation - book not found"""
        self.mock_member_repository.find_by_id.return_value = self.test_member
        self.mock_book_repository.find_by_id.return_value = None
        
        result = self.service.borrow_book("member1", "invalid")
        
        self.assertFalse(result.is_success())
        self.assertEqual("Book not found", result.get_message())
    
    def test_borrow_book_not_available(self):
        """SOLUTION: Test business logic - book not available"""
        self.test_book.set_available(False)
        self.mock_member_repository.find_by_id.return_value = self.test_member
        self.mock_book_repository.find_by_id.return_value = self.test_book
        
        result = self.service.borrow_book("member1", "book1")
        
        self.assertFalse(result.is_success())
        self.assertEqual("Book is not available", result.get_message())
    
    def test_borrow_book_exceeds_limit(self):
        """SOLUTION: Test business rule - borrowing limit"""
        # This tests the new business rule that wasn't in the original code
        self.mock_member_repository.find_by_id.return_value = self.test_member
        self.mock_book_repository.find_by_id.return_value = self.test_book
        
        # Mock member already has 5 books (maximum limit)
        existing_loans = []
        for i in range(5):
            existing_loans.append(Loan(f"loan{i}", "member1", f"book{i}", datetime.now()))
        self.mock_loan_repository.find_by_member_id.return_value = existing_loans
        
        result = self.service.borrow_book("member1", "book1")
        
        self.assertFalse(result.is_success())
        self.assertIn("maximum borrowing limit", result.get_message())
    
    def test_borrow_book_null_inputs(self):
        """SOLUTION: Test input validation - null inputs"""
        # This tests the validation fix from the original code
        result1 = self.service.borrow_book(None, "book1")
        self.assertFalse(result1.is_success())
        self.assertEqual("Member ID cannot be null or empty", result1.get_message())
        
        result2 = self.service.borrow_book("member1", None)
        self.assertFalse(result2.is_success())
        self.assertEqual("Book ID cannot be null or empty", result2.get_message())
    
    def test_borrow_book_empty_inputs(self):
        """SOLUTION: Test input validation - empty inputs"""
        result1 = self.service.borrow_book("", "book1")
        self.assertFalse(result1.is_success())
        self.assertEqual("Member ID cannot be null or empty", result1.get_message())
        
        result2 = self.service.borrow_book("member1", "")
        self.assertFalse(result2.is_success())
        self.assertEqual("Book ID cannot be null or empty", result2.get_message())
    
    # SOLUTION: Integration Tests - End-to-End Scenarios
    # These tests verify that multiple methods work together correctly
    
    def test_complete_borrow_return_flow(self):
        """SOLUTION: Test complete borrowing and returning flow"""
        # This verifies the integration between borrow and return methods
        self.mock_member_repository.find_by_id.return_value = self.test_member
        self.mock_book_repository.find_by_id.return_value = self.test_book
        self.mock_loan_repository.find_by_member_id.return_value = []
        
        # Borrow book
        borrow_result = self.service.borrow_book("member1", "book1")
        self.assertTrue(borrow_result.is_success())
        
        # Return book
        loan = borrow_result.get_loan()
        self.mock_loan_repository.find_by_id.return_value = loan
        self.mock_book_repository.find_by_id.return_value = self.test_book
        
        return_result = self.service.return_book(loan.get_id())
        self.assertTrue(return_result.is_success())
        
        self.mock_loan_repository.delete.assert_called_once_with(loan.get_id())
        self.mock_book_repository.update.assert_called_with(self.test_book)
    
    def test_get_available_books(self):
        """SOLUTION: Test get available books method"""
        all_books = [
            Book("book1", "Title 1", "Author 1"),
            Book("book2", "Title 2", "Author 2")
        ]
        all_books[1].set_available(False)  # Make second book unavailable
        
        self.mock_book_repository.find_all.return_value = all_books
        
        available_books = self.service.get_available_books()
        
        self.assertEqual(1, len(available_books))
        self.assertEqual("book1", available_books[0].get_id())
    
    def test_get_member_loans(self):
        """SOLUTION: Test get member loans method"""
        member_loans = [
            Loan("loan1", "member1", "book1", datetime.now()),
            Loan("loan2", "member1", "book2", datetime.now())
        ]
        
        self.mock_loan_repository.find_by_member_id.return_value = member_loans
        
        result = self.service.get_member_loans("member1")
        
        self.assertEqual(2, len(result))
        self.assertEqual("loan1", result[0].get_id())
        self.assertEqual("loan2", result[1].get_id())
    
    # SOLUTION: Edge Case Tests - Boundary Conditions
    # These tests verify behavior at the boundaries of valid inputs
    
    def test_get_member_loans_null_input(self):
        """SOLUTION: Test null input handling"""
        result = self.service.get_member_loans(None)
        self.assertTrue(len(result) == 0)
    
    def test_get_member_loans_empty_input(self):
        """SOLUTION: Test empty input handling"""
        result = self.service.get_member_loans("")
        self.assertTrue(len(result) == 0)
    
    def test_calculate_fine_null_input(self):
        """SOLUTION: Test null input handling"""
        fine = self.service.calculate_fine(None)
        self.assertEqual(0.0, fine)
    
    def test_calculate_fine_empty_input(self):
        """SOLUTION: Test empty input handling"""
        fine = self.service.calculate_fine("")
        self.assertEqual(0.0, fine)
    
    def test_calculate_fine_loan_not_found(self):
        """SOLUTION: Test loan not found scenario"""
        self.mock_loan_repository.find_by_id.return_value = None
        
        fine = self.service.calculate_fine("invalid")
        self.assertEqual(0.0, fine)
    
    def test_calculate_fine_with_strategy(self):
        """SOLUTION: Test fine calculation with strategy pattern"""
        loan = Loan("loan1", "member1", "book1", datetime.now())
        self.mock_loan_repository.find_by_id.return_value = loan
        self.mock_fine_strategy.calculate_fine.return_value = 5.0
        
        fine = self.service.calculate_fine("loan1")
        self.assertEqual(5.0, fine)
        self.mock_fine_strategy.calculate_fine.assert_called_once_with(loan, 14)
    
    # SOLUTION: Business Logic Tests - Business Rules
    # These tests verify that business rules are enforced correctly
    
    def test_add_book_validation(self):
        """SOLUTION: Test add book with validation"""
        self.assertTrue(self.service.add_book(self.test_book))
        self.mock_book_repository.save.assert_called_once_with(self.test_book)
    
    def test_add_book_null_book(self):
        """SOLUTION: Test add book with null input"""
        self.assertFalse(self.service.add_book(None))
    
    def test_add_book_null_id(self):
        """SOLUTION: Test add book with null ID"""
        book_with_null_id = Book(None, "Title", "Author")
        self.assertFalse(self.service.add_book(book_with_null_id))
    
    def test_add_member_validation(self):
        """SOLUTION: Test add member with validation"""
        self.assertTrue(self.service.add_member(self.test_member))
        self.mock_member_repository.save.assert_called_once_with(self.test_member)
    
    def test_add_member_null_member(self):
        """SOLUTION: Test add member with null input"""
        self.assertFalse(self.service.add_member(None))
    
    def test_add_member_null_id(self):
        """SOLUTION: Test add member with null ID"""
        member_with_null_id = Member(None, "Name", "email@example.com")
        self.assertFalse(self.service.add_member(member_with_null_id))
    
    # SOLUTION: Error Handling Tests - Exception Scenarios
    # These tests verify that exceptions are handled gracefully
    
    def test_borrow_book_repository_exception(self):
        """SOLUTION: Test exception handling in borrow book"""
        self.mock_member_repository.find_by_id.side_effect = Exception("Database error")
        
        result = self.service.borrow_book("member1", "book1")
        
        self.assertFalse(result.is_success())
        self.assertIn("Failed to borrow book", result.get_message())
    
    def test_return_book_repository_exception(self):
        """SOLUTION: Test exception handling in return book"""
        self.mock_loan_repository.find_by_id.side_effect = Exception("Database error")
        
        result = self.service.return_book("loan1")
        
        self.assertFalse(result.is_success())
        self.assertIn("Failed to return book", result.get_message())
    
    def test_get_available_books_exception(self):
        """SOLUTION: Test exception handling in get available books"""
        self.mock_book_repository.find_all.side_effect = Exception("Database error")
        
        result = self.service.get_available_books()
        
        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
