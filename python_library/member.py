from typing import Optional


class Member:
    def __init__(self, member_id: str, name: str, email: str):
        self.id = member_id
        self.name = name
        self.email = email
    
    def get_id(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_email(self) -> str:
        return self.email
