from abc import ABC, abstractmethod
from dao.user_module.user import User
from typing import List, Optional


class IUserDAO(ABC):
    @abstractmethod
    def save(self, user: User) -> bool:
        pass

    @abstractmethod
    def findById(self, userId: str) -> Optional[User]:
        pass

    @abstractmethod
    def findByEmail(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def findAll(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> bool:
        pass

    @abstractmethod
    def delete(self, userId: str) -> bool:
        pass