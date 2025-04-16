from typing import Optional, List, Dict
from backend.dao.management_dao import User, ManagementDAO
from backend.utils.hasher import get_password_hash, verify_password
from backend.knowledge.auth.iauth_manager import IAuthManager


class AuthManager(IAuthManager):
    def __init__(self, management_dao: ManagementDAO):
        self._dao = management_dao

    def check_existing_user(self, email: str) -> bool:
        try:
            return self._dao.findUserByEmail(email) is not None
        except Exception:
            return False

    def create_new_user(self, email: str, password: str, name: str, department_id: str,
                        roles: List[str]) -> bool:
        if self.check_existing_user(email):
            return False

        # Hash the password
        hashed_password = get_password_hash(password=password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            departmentId=department_id,
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

        return verify_password(password, hashed)

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
