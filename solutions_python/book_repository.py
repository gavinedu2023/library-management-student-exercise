from abc import ABC, abstractmethod
from typing import List, Optional

from ..python_library.book import Book


class BookRepository(ABC):
    """
    SOLUTION: Repository Pattern Interface
    
    This interface abstracts data access operations for books.
    Benefits:
    1. Separates business logic from data storage
    2. Makes testing easier with mock implementations
    3. Allows switching between different data sources
    4. Improves maintainability and extensibility
    """
    
    @abstractmethod
    def save(self, book: Book) -> None:
        """Save a book to the repository"""
        pass
    
    @abstractmethod
    def find_by_id(self, book_id: str) -> Optional[Book]:
        """Find a book by its ID"""
        pass
    
    @abstractmethod
    def update(self, book: Book) -> None:
        """Update an existing book in the repository"""
        pass
    
    @abstractmethod
    def delete(self, book_id: str) -> None:
        """Delete a book from the repository"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Book]:
        """Get all books from the repository"""
        pass
