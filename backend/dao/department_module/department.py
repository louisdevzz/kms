from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from bson import ObjectId

from backend.dao.department_module.interface import IDepartment


class Department(BaseModel, IDepartment):
    departmentId: str = Field(..., description="Unique identifier for the department_module")
    name: str = Field(..., description="Name of the department_module")
    description: str = Field(..., description="Description of the department_module")

    def __init__(self, name: str, description: str):
        super().__init__(
            department_id=str(ObjectId()),
            name=name,
            description=description
        )

    def to_json(self) -> str:
        return self.model_dump_json()

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def set_name(self, new_name: str) -> bool:
        if new_name:
            self.name = new_name.strip()
            return True
        return False

    def set_description(self, new_description: str) -> bool:
        if new_description:
            self.description = new_description
            return True
        return False