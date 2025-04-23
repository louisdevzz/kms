from typing import List
from dao.management_dao import ManagementDAO
from knowledge.permission.iper_manager import IPermissionManager
from dao.permission_module.permission import Permission


class PermissionManager(IPermissionManager):
    def __init__(self, management_dao: ManagementDAO):
        self._dao = management_dao

    def get_docId_by_userId(self, user_id: str) -> List[str]:
        user_permissions = self._dao.getPermissionsByUser(user_id)
        doc_ids = list({permission.docId for permission in user_permissions})
        return doc_ids

    def get_permissions_by_user(self, user_id: str) -> List[Permission]:
        try:
            permissions = self._dao.getPermissionsByUser(user_id=user_id)
            return permissions
        except Exception:
            return []

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
            # validate permissions
            if not self._validate_permissions(permissions):
                return False

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
