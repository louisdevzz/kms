from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from backend.dao.managementdao import User
from backend.dao.managementdao import ManagementDAO
from backend.utils.hasher import PasswordHasher


class IAuthManager(ABC):
    @abstractmethod
    def check_existing_user(self, email: str) -> bool: pass

    @abstractmethod
    def create_new_user(self, email: str, password: str, name: str, department_id: str,
                        roles: List[Dict[str, str]]) -> bool: pass

    @abstractmethod
    def check_password(self, email: str, password: str) -> bool: pass

    @abstractmethod
    def get_user_information(self, user_id: str) -> Optional[User]: pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]: pass


class AuthManager(IAuthManager):
    def __init__(self, management_dao: ManagementDAO):
        self._dao = management_dao

    def check_existing_user(self, email: str) -> bool:
        try:
            return self._dao.findUserByEmail(email) is not None
        except Exception:
            return False

    def create_new_user(self, email: str, password: str, name: str, department_id: str,
                        roles: List[Dict[str, str]]) -> bool:
        if self.check_existing_user(email):
            return False

        # Hash the password
        hashed_password = PasswordHasher.get_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            department_id=department_id,
            roles=roles
        )

        return self._dao.saveUser(new_user)

    def check_password(self, email: str, password: str) -> bool:
        user = self._dao.findUserByEmail(email)
        if not user:
            return False

        try:
            hashed = user.get_password()
        except ValueError:
            return False

        return PasswordHasher.verify_password(password, hashed)

    def get_user_information(self, user_id: str) -> Optional[User]:
        try:
            user_data = self._dao.findUserById(user_id)
            if not user_data:
                return None
            return user_data
        except Exception:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            user = self._dao.findUserByEmail(email)
            if not user:
                return None
            return user
        except Exception:
            return None
