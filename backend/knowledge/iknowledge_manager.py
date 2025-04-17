from abc import ABC, abstractmethod
from typing import Dict, List, Optional, BinaryIO
from backend.dao.management_dao import User, Document, Version


class IKnowledgeManager(ABC):
    # auth
    @abstractmethod
    def sign_up(self, email: str, password: str, name: str, department_id: str, roles: List[str]) -> bool: pass

    @abstractmethod
    def login(self, email: str, password: str) -> bool: pass

    @abstractmethod
    def get_user_information(self, user_id: str) -> Optional[User]: pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]: pass

    # doc
    @abstractmethod
    def upload(self, content: BinaryIO, name: str, doc_type: str,
               department_id: str, tags: List[str], owner: str,
               category: str, description: str, university: str) -> dict: pass

    @abstractmethod
    def get_metadata(self, document_id: str, user_id: str) -> Dict[str, object]: pass

    @abstractmethod
    def get_content(self, document_id: str, user_id: str) -> Optional[BinaryIO]: pass

    @abstractmethod
    def get_doc_ids(self, user_id: str) -> List[str]:pass

    @abstractmethod
    def update_metadata(self, modified_by: str, document_id: str, new_name: str,
                        new_department_id: str, new_tags: List[str],
                        new_owner: str, new_category: str,
                        new_description: str, new_university: str) -> bool: pass

    @abstractmethod
    def update_content(self, document_id: str, modified_by: str, new_content: BinaryIO) -> bool: pass

    @abstractmethod
    def delete(self, deleted_by: str, document_id: str) -> bool: pass

    @abstractmethod
    def get_all_metadata(self) -> Dict[str, Dict[str, object]]: pass

    @abstractmethod
    def get_all_versions(self, user_id: str, document_id: str) -> List[Version]: pass

    @abstractmethod
    def get_specific_version(self, user_id: str, document_id: str, version_number: int) -> Optional[Document]: pass

    @abstractmethod
    def restore_version(self, document_id: str, restored_by: str, version_number: int) -> bool: pass

    # permission
    @abstractmethod
    def share_permissions(self, shared_by: str, shared_to: str, document_id: str, permissions: List[str]) -> bool: pass

    @abstractmethod
    def remove_permissions(self, removed_by: str, removed_to: str, document_id: str, permissions: List[str]) -> bool: pass
