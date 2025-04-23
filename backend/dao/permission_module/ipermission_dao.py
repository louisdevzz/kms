from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.permission_module.permission import Permission


class IPermissionDAO(ABC):
    @abstractmethod
    def save(self, permission: Permission) -> bool: pass

    @abstractmethod
    def findByUser(self, userId: str) -> List[Permission]: pass

    @abstractmethod
    def findByDoc(self, docId: str, session=None) -> List[Permission]: pass

    @abstractmethod
    def findByUserDoc(self, userId: str, docId: str) -> Optional[Permission]: pass

    @abstractmethod
    def findAll(self) -> List[Permission]: pass

    @abstractmethod
    def update(self, permission: Permission) -> bool: pass

    @abstractmethod
    def delete(self, permissionId: str, session=None) -> bool: pass