from abc import ABC, abstractmethod
from typing import List, Optional

from ..python_library.member import Member


class MemberRepository(ABC):
    """
    SOLUTION: Repository Pattern Interface for Members
    """
    
    @abstractmethod
    def save(self, member: Member) -> None:
        """Save a member to the repository"""
        pass
    
    @abstractmethod
    def find_by_id(self, member_id: str) -> Optional[Member]:
        """Find a member by their ID"""
        pass
    
    @abstractmethod
    def update(self, member: Member) -> None:
        """Update an existing member in the repository"""
        pass
    
    @abstractmethod
    def delete(self, member_id: str) -> None:
        """Delete a member from the repository"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Member]:
        """Get all members from the repository"""
        pass
