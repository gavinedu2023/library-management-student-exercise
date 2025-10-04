import unittest
from unittest import TestCase

from .library_service import LibraryService
from .book import Book
from .member import Member


class LibraryServiceTest(TestCase):
    
    def setUp(self):
        self.service = LibraryService()
        
        # Add test data
        self.service.add_member(Member("member1", "John Doe", "john@example.com"))
        self.service.add_book(Book("book1", "Java Programming", "Author Name"))
    
    def test_borrow_book_success(self):
        result = self.service.borrow_book("member1", "book1")
        self.assertIn("Book borrowed successfully", result)
    
    def test_borrow_book_member_not_found(self):
        result = self.service.borrow_book("invalid", "book1")
        self.assertEqual("Member not found", result)


if __name__ == '__main__':
    unittest.main()
