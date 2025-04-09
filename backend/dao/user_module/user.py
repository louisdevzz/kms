from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Dict, Optional


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


class User(BaseModel, IUser):
    userId: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of user_module")
    email: str = Field(..., description="Email of user_module")
    password: str = Field(..., description="Password hash")
    departmentId: str = Field(..., description="Department ID (single department_module)")
    roles: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of roles with name and description"
    )

    def __init__(
            self,
            name: str,
            email: str,
            password: str,
            departmentId: str,
            roles: Optional[List[Dict[str, str]]] = None,
            **kwargs
    ):
        roles = roles or []

        super().__init__(
            userId=str(ObjectId()),
            name=name,
            email=email,
            password=password,
            departmentId=departmentId,
            roles=roles,
            **kwargs
        )

    def to_json(self) -> str:
        return self.model_dump_json()

    # Password methods
    def verify_password(self, password: str) -> bool:
        return self.password == password

    def get_password(self) -> str:
        return self.password

    def set_password(self, new_password: str) -> bool:
        if new_password:
            self.password = new_password
            return True
        return False

    # Department methods
    def get_departmentID(self) -> str:
        return self.departmentId

    def set_departmentID(self, newDepartmentId: str) -> bool:
        if newDepartmentId:
            self.departmentId = newDepartmentId
            return True
        return False

    # role methods
    def get_roles(self) -> List[Dict[str, str]]:
        return self.roles

    def add_role(self, role_name: str, role_description: str = "") -> bool:
        if not any(r['name'] == role_name for r in self.roles):
            self.roles.append({
                'name': role_name,
                'description': role_description
            })
            return True
        return False

    def remove_role(self, role_name: str) -> bool:
        initial_count = len(self.roles)
        self.roles = [r for r in self.roles if r['name'] != role_name]
        return len(self.roles) < initial_count

    def has_role(self, role_name: str) -> bool:
        return any(r['name'] == role_name for r in self.roles)