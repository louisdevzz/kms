from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from dao.management_dao import User


class IAuthManager(ABC):
    @abstractmethod
    def check_existing_user(self, email: str) -> bool: pass

    @abstractmethod
    def create_new_user(self, email: str, password: str, name: str, department_id: str,
                        roles: List[str]) -> bool: pass

    @abstractmethod
    def check_password(self, email: str, password: str) -> bool: pass

    @abstractmethod
    def get_user_information(self, user_id: str) -> Optional[User]: pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]: pass