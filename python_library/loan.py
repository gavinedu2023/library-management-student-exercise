from datetime import datetime
from typing import Optional


class Loan:
    def __init__(self, loan_id: str, member_id: str, book_id: str, borrow_date: datetime):
        self.id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
    
    def get_id(self) -> str:
        return self.id
    
    def get_member_id(self) -> str:
        return self.member_id
    
    def get_book_id(self) -> str:
        return self.book_id
    
    def get_borrow_date(self) -> datetime:
        return self.borrow_date
