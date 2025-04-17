from typing import Dict, List, Optional, BinaryIO
from backend.knowledge.auth.auth_manager import AuthManager
from backend.knowledge.document.doc_manager import DocumentManager
from backend.knowledge.permission.per_manager import PermissionManager
from backend.dao.management_dao import ManagementDAO, User, Document, Version
from backend.knowledge.iknowledge_manager import IKnowledgeManager


class KnowledgeManager(IKnowledgeManager):
    def __init__(self):
        self.dao = ManagementDAO()
        self._perms = PermissionManager(self.dao)
        self._auth = AuthManager(self.dao)
        self._docs = DocumentManager(self.dao)

    # Authentication
    def sign_up(self, email: str, password: str, name: str, department_id: str, roles: List[str]) -> bool:
        return self._auth.create_new_user(
            email=email,
            password=password,
            name=name,
            department_id=department_id,
            roles=roles
        )

    def login(self, email: str, password: str) -> bool:
        return self._auth.check_password(email, password)

    def get_user_information(self, user_id: str) -> Optional[User]:
        return self._auth.get_user_information(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self._auth.get_user_by_email(email)

    # Document
    def upload(self, content: BinaryIO, name: str, doc_type: str,
               department_id: str, tags: List[str], owner: str,
               category: str, description: str, university: str) -> dict:
        return self._docs.upload(
            content=content,
            name=name,
            doc_type=doc_type,
            department_id=department_id,
            tags=tags,
            owner=owner,
            category=category,
            description=description,
            university=university
        )

    def get_metadata(self, document_id: str, user_id: str) -> Dict[str, object]:
        if not self._perms.has_permission(user_id=user_id, document_id=document_id, required="read"):
            raise PermissionError("User does not have permission to read the document.")
        return self._docs.get_metadata(document_id=document_id, user_id=user_id)

    def get_content(self, document_id: str, user_id: str) -> Optional[BinaryIO]:
        if not self._perms.has_permission(user_id=user_id, document_id=document_id, required="read"):
            raise PermissionError("User does not have permission to read the document.")
        return self._docs.get_content(document_id=document_id, user_id=user_id)

    def get_doc_ids(self, user_id: str) -> List[str]:
        document_ids = self._perms.get_docId_by_userId(user_id)
        return document_ids

    def update_metadata(self, modified_by: str, document_id: str, new_name: str,
                        new_department_id: str, new_tags: List[str],
                        new_owner: str, new_category: str,
                        new_description: str, new_university: str) -> bool:

        if not self._perms.has_permission(user_id=modified_by, document_id=document_id, required="write"):
            raise PermissionError("User does not have permission to write the document.")
        return self._docs.update_metadata(
            modified_by=modified_by,
            document_id=document_id,
            new_name=new_name,
            new_department_id=new_department_id,
            new_tags=new_tags,
            new_owner=new_owner,
            new_category=new_category,
            new_description=new_description,
            new_university=new_university
        )

    def update_content(self, document_id: str, modified_by: str, new_content: BinaryIO) -> bool:
        if not self._perms.has_permission(user_id=modified_by, document_id=document_id, required="write"):
            raise PermissionError("User does not have permission to write the document.")
        return self._docs.update_content(
            modified_by=modified_by,
            document_id=document_id,
            new_content=new_content
        )

    def delete(self, deleted_by: str, document_id: str) -> bool:
        if not self._perms.has_permission(user_id=deleted_by, document_id=document_id, required="delete"):
            raise PermissionError("User does not have permission to delete the document.")
        return self._docs.delete(deleted_by=deleted_by, document_id=document_id)

    def get_all_metadata(self) -> Dict[str, Dict[str, object]]:
        return self._docs.get_all_metadata()

    def get_all_versions(self, user_id: str, document_id: str) -> List[Version]:
        return self._docs.get_all_versions(user_id=user_id, document_id=document_id)

    def get_specific_version(self, user_id: str, document_id: str, version_number: int) -> Optional[Document]:
        return self._docs.get_specific_version(user_id=user_id, document_id=document_id, version_number=version_number)

    def restore_version(self, document_id: str, restored_by: str, version_number: int) -> bool:
        return self._docs.restore_version(
            document_id=document_id,
            restored_by=restored_by,
            version_number=version_number
        )

    # Permission
    def share_permissions(self, shared_by: str, shared_to: str, document_id: str, permissions: List[str]) -> bool:
        return self._perms.share_permissions(
            shared_by=shared_by,
            shared_to=shared_to,
            document_id=document_id,
            permissions=permissions
        )

    def remove_permissions(self, removed_by: str, removed_to: str, document_id: str,permissions: List[str]) -> bool:
        return self._perms.remove_permissions(
            removed_by=removed_by,
            removed_to=removed_to,
            document_id=document_id,
            permissions=permissions
        )