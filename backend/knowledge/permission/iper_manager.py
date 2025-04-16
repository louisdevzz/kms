from abc import ABC, abstractmethod
from typing import List


class IPermissionManager(ABC):
    @abstractmethod
    def get_permissions(self, user_id: str, document_id: str) -> List[str]:
        pass

    @abstractmethod
    def has_permission(self, user_id: str, document_id: str, required: str) -> bool:
        pass

    @abstractmethod
    def share_permissions(self, shared_by: str, shared_to: str, document_id: str, permissions: List[str]) -> bool:
        pass

    @abstractmethod
    def remove_permissions(self, removed_by: str, removed_to: str, document_id: str, permissions: List[str]) -> bool:
        pass