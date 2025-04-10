from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.department_module.department import Department


class IDepartmentDAO(ABC):
    @abstractmethod
    def save(self, department: Department) -> bool: pass

    @abstractmethod
    def findById(self, departmentId: str) -> Optional[Department]: pass

    @abstractmethod
    def findAll(self) -> List[Department]: pass

    @abstractmethod
    def update(self, department: Department) -> bool: pass

    @abstractmethod
    def delete(self, departmentId: str) -> bool: pass