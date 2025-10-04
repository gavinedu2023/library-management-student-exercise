# Library Management System - Python Implementation

This is a Python translation of the Java library management system.

## Files

- `book.py` - Book class with id, title, author, and availability status
- `member.py` - Member class with id, name, and email
- `loan.py` - Loan class tracking book loans with dates
- `library_service.py` - Main service class handling library operations
- `test_library_service.py` - Unit tests for the library service
- `__init__.py` - Package initialization file

## Usage

```python
from python_library import LibraryService, Book, Member

# Create service
service = LibraryService()

# Add a member
member = Member("member1", "John Doe", "john@example.com")
service.add_member(member)

# Add a book
book = Book("book1", "Python Programming", "Author Name")
service.add_book(book)

# Borrow a book
result = service.borrow_book("member1", "book1")
print(result)

# Return a book
result = service.return_book(loan_id)
print(result)
```

## Running Tests

```bash
python -m unittest python_library.test_library_service
```

## Features

- Book management (add, borrow, return)
- Member management
- Loan tracking with fine calculation
- Available books listing
- Member loan history
