import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from .book import Book
from .member import Member
from .loan import Loan


class LibraryService:
    def __init__(self):
        self.books: List[Book] = []
        self.members: List[Member] = []
        self.loans: List[Loan] = []
    
    def borrow_book(self, member_id: str, book_id: str) -> str:
        try:
            # Find member
            member = None
            for m in self.members:
                if m.get_id() == member_id:
                    member = m
                    break
            
            if member is None:
                return "Member not found"
            
            # Find book
            book = None
            for b in self.books:
                if b.get_id() == book_id:
                    book = b
                    break
            
            if book is None:
                return "Book not found"
            
            # Check if book is available
            if not book.is_available():
                return "Book is not available"
            
            # Create loan
            loan_id = str(uuid.uuid4())
            loan = Loan(loan_id, member_id, book_id, datetime.now())
            self.loans.append(loan)
            
            # Update book status
            book.set_available(False)
            
            return f"Book borrowed successfully. Loan ID: {loan_id}"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def return_book(self, loan_id: str) -> str:
        try:
            # Find loan
            loan = None
            for l in self.loans:
                if l.get_id() == loan_id:
                    loan = l
                    break
            
            if loan is None:
                return "Loan not found"
            
            # Find book
            book = None
            for b in self.books:
                if b.get_id() == loan.get_book_id():
                    book = b
                    break
            
            if book is not None:
                book.set_available(True)
            
            # Remove loan
            self.loans.remove(loan)
            
            return "Book returned successfully"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_available_books(self) -> List[Book]:
        available_books = []
        for book in self.books:
            if book.is_available():
                available_books.append(book)
        return available_books
    
    def get_member_loans(self, member_id: str) -> List[Loan]:
        member_loans = []
        for loan in self.loans:
            if loan.get_member_id() == member_id:
                member_loans.append(loan)
        return member_loans
    
    def add_book(self, book: Book) -> None:
        self.books.append(book)
    
    def add_member(self, member: Member) -> None:
        self.members.append(member)
    
    def calculate_fine(self, loan_id: str) -> float:
        loan = None
        for l in self.loans:
            if l.get_id() == loan_id:
                loan = l
                break
        
        if loan is None:
            return 0.0
        
        # Calculate days overdue
        days_overdue = (datetime.now() - loan.get_borrow_date()).days
        
        if days_overdue > 14:
            return (days_overdue - 14) * 0.50  # $0.50 per day after 14 days
        
        return 0.0
