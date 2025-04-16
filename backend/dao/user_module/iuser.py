from abc import ABC, abstractmethod
from typing import List, Dict


class IUser(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str) -> bool:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass

    @abstractmethod
    def get_departmentID(self) -> str:
        pass

    @abstractmethod
    def set_password(self, new_password: str) -> bool:
        pass

    @abstractmethod
    def set_departmentID(self, newDepartmentId: str) -> bool:
        pass

    @abstractmethod
    def get_roles(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def add_role(self, role_name: str, role_description: str = "") -> bool:
        pass

    @abstractmethod
    def remove_role(self, role_name: str) -> bool:
        pass

    @abstractmethod
    def has_role(self, role_name: str) -> bool:
        pass
