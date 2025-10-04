from datetime import datetime
from typing import Optional


class Book:
    def __init__(self, book_id: str, title: str, author: str):
        self.id = book_id
        self.title = title
        self.author = author
        self.available = True
    
    def get_id(self) -> str:
        return self.id
    
    def get_title(self) -> str:
        return self.title
    
    def get_author(self) -> str:
        return self.author
    
    def is_available(self) -> bool:
        return self.available
    
    def set_available(self, available: bool) -> None:
        self.available = available
