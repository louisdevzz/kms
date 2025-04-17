from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials


class IAPIRouter(ABC):
    @abstractmethod
    async def sign_up(
            self,
            email: str,
            password: str,
            name: str,
            department_id: str,
            roles: List[str]
    ) -> dict: pass

    @abstractmethod
    async def login(
            self,
            email: str,
            password: str
    ) -> dict: pass

    @abstractmethod
    async def upload_document(
            self,
            document: UploadFile,
            name: Optional[str],
            doc_type: Optional[str],
            department_id: Optional[str],
            tags: Optional[List[str]],
            owner: Optional[str],
            category: Optional[str],
            description: Optional[str],
            university: Optional[str],
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def get_current_user(
            self,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def get_document_meta(
            self,
            document_id: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def get_document_content(
            self,
            document_id: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def update_document_meta(
            self,
            modified_by: str,
            document_id: str,
            new_name: str,
            new_department_id: str,
            new_tags: List[str],
            new_owner: str,
            new_category: str,
            new_description: str,
            new_university: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def update_document_content(
            self,
            document_id: str,
            modified_by: str,
            document: UploadFile,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def delete_document(
            self,
            deleted_by: str,
            document_id: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def get_document_versions(
            self,
            user_id: str,
            document_id: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def get_specific_document_version(
            self,
            user_id: str,
            document_id: str,
            version_number: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def restore_document_version(
            self,
            document_id: str,
            version_number: str,
            restored_by: str,
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def share_document_permission(
            self,
            shared_by: str,
            shared_to: str,
            document_id: str,
            permissions: List[str],
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass

    @abstractmethod
    async def remove_document_permission(
            self,
            removed_by: str,
            removed_to: str,
            document_id: str,
            permissions: List[str],
            credentials: HTTPAuthorizationCredentials
    ) -> dict: pass
