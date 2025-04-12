from abc import ABC, abstractmethod
from typing import Dict, List, Optional, BinaryIO
from backend.dao.management_dao import Document, Version
from backend.dao.management_dao import ManagementDAO
from backend.knowledge.permissionmanager import PermissionManager


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


class DocumentManager(IDocumentManager):
    def __init__(self, management_dao: ManagementDAO):
        self._dao = management_dao

    def upload(self, content: BinaryIO, name: str, doc_type: str, department_id: str,
               tags: List[str], owner: str, category: str,
               description: str, university: str) -> dict:
        try:
            content.seek(0, 2)
            file_size = content.tell()
            content.seek(0)

            doc = Document(
                name=name,
                owner=owner,
                dType=doc_type,
                departmentId=department_id,
                description=description,
                university=university,
                file_size=file_size,
                tags=[tags] if tags else [],
                category=[category] if category else []
            )
            result = self._dao.saveDocument(doc, content)
            return result
        except Exception:
            return []

    def get_metadata(self, document_id: str, user_id: str) -> Dict[str, object]:
        # check permission before find document
        if not PermissionManager.has_permission(user_id=user_id, document_id=document_id, required="read"):
            raise PermissionError("User does not have permission to read the document.")

        doc = self._dao.findDocumentById(document_id)
        return doc.model_dump(exclude={'versions'}) if doc else {}

    def get_content(self, document_id: str, user_id: str) -> Optional[BinaryIO]:
        # check permission before find document
        if not PermissionManager.has_permission(user_id=user_id, document_id=document_id, required="read"):
            raise PermissionError("User does not have permission to read the document.")

        return self._dao.get_document_content(document_id)

    def update_metadata(self, modified_by: str, document_id: str, new_name: str, new_department_id: str, new_tags: List[str],
                        new_owner: str, new_category: List[str], new_description: str, new_university: str) -> bool:
        # check permission before update metadata
        if not PermissionManager.has_permission(user_id=modified_by, document_id=document_id, required="write"):
            raise PermissionError("User does not have permission to write the document.")

        # find doc
        doc = self._dao.findDocumentById(document_id)
        if not doc:
            return False

        # update doc
        doc.name = new_name
        doc.departmentId = new_department_id
        doc.tags = new_tags
        doc.owner = new_owner
        doc.category = new_category
        doc.description = new_description
        doc.university = new_university
        return self._dao.updateMetaData(doc)

    def update_content(self, modified_by: str, document_id: str, new_content: BinaryIO) -> bool:
        # check permission before update content
        if not PermissionManager.has_permission(user_id=modified_by, document_id=document_id, required="write"):
            raise PermissionError("User does not have permission to write the document.")

        # find doc
        doc = self._dao.findDocumentById(document_id)

        if not doc:
            return False
        # get file's size
        new_content.seek(0, 2)
        file_size = new_content.tell()
        new_content.seek(0)

        return self._dao.update_content(modified_by, document_id, new_content, file_size)

    def delete(self, deleted_by: str, document_id: str) -> bool:
        # check permission before delete document
        if not PermissionManager.has_permission(user_id=deleted_by, document_id=document_id, required="delete"):
            raise PermissionError("User does not have permission to delete the document.")

        return self._dao.deleteDocument(document_id)

    def get_all_metadata(self) -> Dict[str, Dict[str, object]]:
        docs = self._dao.findAllDocuments()
        return {doc.documentId: doc.model_dump(exclude={'versions'}) for doc in docs}

    def get_all_versions(self, user_id: str, document_id: str) -> List[Version]:
        # check permission before read document
        if not PermissionManager.has_permission(user_id=user_id, document_id=document_id, required="read"):
            raise PermissionError("User does not have permission to read the document.")

        doc = self._dao.findDocumentById(document_id)
        return doc.versions if doc else []

    def get_specific_version(self, user_id: str, document_id: str, version_number: int) -> Optional[Document]:
        # check permission before read document
        if not PermissionManager.has_permission(user_id=user_id, document_id=document_id, required="read"):
            raise PermissionError("User does not have permission to read the document.")

        # find doc
        doc = self._dao.findDocumentById(document_id)

        if not doc:
            return None
        version = next((v for v in doc.versions if v.version_number == version_number), None)  # find version
        if not version:
            return None
        versioned_doc = doc.model_copy()
        versioned_doc.versions = [version]
        versioned_doc.currentNumber = version_number
        return versioned_doc

    def restore_version(self, document_id: str, restored_by: str, version_number: int) -> bool:
        # check permission before read document
        if not PermissionManager.has_permission(user_id=restored_by, document_id=document_id, required="write"):
            raise PermissionError("User does not have permission to restore the document.")

        # find doc
        doc = self._dao.findDocumentById(document_id)

        if not doc:
            return False
        version = next((v for v in doc.versions if v.version_number == version_number), None)  # find version
        if not version:
            return False

        old_content = self._dao.get_document_content(document_id, version_number)  # find old content
        if not old_content:
            return False
        return self.update_content(document_id=document_id, modified_by=restored_by, new_content=old_content)
