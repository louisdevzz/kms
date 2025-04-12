from abc import ABC, abstractmethod
from typing import List
from backend.dao.management_dao import ManagementDAO


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


class PermissionManager(IPermissionManager):
    def __init__(self, management_dao: ManagementDAO):
        self._dao = management_dao

    def get_permissions(self, user_id: str, document_id: str) -> List[str]:
        try:
            permissions = self._dao.getPermissionsByUserDoc(user_id, document_id)
            return permissions.permissions if permissions else []
        except Exception:
            return []

    def has_permission(self, user_id: str, document_id: str, required: str) -> bool:
        try:
            if required not in {"read", "write", "share", "delete"}:
                return False

            permissions = self.get_permissions(user_id, document_id)
            return required in permissions
        except Exception:
            return False

    def share_permissions(self, shared_by: str, shared_to: str, document_id: str, permissions: List[str]) -> bool:
        try:
            # check permission before share
            if not self.has_permission(user_id=shared_by, document_id=document_id, required="share"):
                raise PermissionError("User does not have permission to share the document.")

            # validate permissions
            if not self._validate_permissions(permissions):
                return False

            existing = self._dao.getPermissionsByUserDoc(user_id=shared_to, doc_id=document_id)
            new_perms = [p for p in permissions if p not in existing.permissions]

            if not new_perms:
                return True  # No new permissions to add

            return self._dao.shareDocument(document_id=document_id, user_id=shared_to, permissions=permissions)
        except Exception:
            return False

    def remove_permissions(self, removed_by: str, removed_to: str, document_id: str, permissions: List[str]) -> bool:
        try:
            # check permission before share
            if not self.has_permission(user_id=removed_by, document_id=document_id, required="share"):
                raise PermissionError("User does not have permission to remove share on this document.")

            # validate permissions
            if not self._validate_permissions(permissions):
                return False

            return self._dao.removeShareDocument(document_id=document_id, user_id=removed_to, permissions=permissions)
        except Exception:
            return False

    @staticmethod
    def _validate_permissions(permissions: List[str]) -> bool:
        valid_perms = {"read", "write", "share", "delete"}
        return all(p in valid_perms for p in permissions)
