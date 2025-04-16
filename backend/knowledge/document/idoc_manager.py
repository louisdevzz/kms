from abc import ABC, abstractmethod
from typing import Dict, List, Optional, BinaryIO
from backend.dao.management_dao import Document, Version


class IDocumentManager(ABC):
    @abstractmethod
    def upload(self, content: BinaryIO, name: str, doc_type: str, department_id: str,
               tags: List[str], owner: str, category: str, description: str, university: str) -> dict: pass

    @abstractmethod
    def get_metadata(self, document_id: str, user_id: str) -> Dict[str, object]: pass

    @abstractmethod
    def get_content(self, document_id: str, user_id: str) -> Optional[BinaryIO]: pass

    @abstractmethod
    def update_metadata(self, modified_by: str, document_id: str, new_name: str, new_department_id: str, new_tags: List[str],
                        new_owner: str, new_category: List[str], new_description: str, new_university: str) -> bool: pass

    @abstractmethod
    def update_content(self, modified_by: str, document_id: str, new_content: BinaryIO) -> bool: pass

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

