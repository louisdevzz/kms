from abc import ABC, abstractmethod
from typing import List, Optional, BinaryIO
from backend.dao.user_module.user import User
from backend.dao.document_module.document import Document, Version
from backend.dao.department_module.department import Department
from backend.dao.activitylog_module.activitylog import ActivityLog
from backend.dao.permission_module.permission import Permission


class IManagementDAO(ABC):
    @abstractmethod
    def close_connection(self): pass

    # User
    @abstractmethod
    def saveUser(self, user: User) -> bool: pass

    @abstractmethod
    def findUserById(self, user_id: str) -> Optional[User]: pass

    @abstractmethod
    def findUserByEmail(self, email: str) -> Optional[User]: pass

    @abstractmethod
    def findAllUsers(self) -> List[User]: pass

    @abstractmethod
    def updateUser(self, user: User) -> bool: pass

    @abstractmethod
    def deleteUser(self, user_id: str) -> bool: pass

    # Document
    @abstractmethod
    def saveDocument(self, document: Document, content: Optional[BinaryIO] = None) -> dict: pass

    @abstractmethod
    def get_document_content(self, document_id: str, version_num: Optional[int] = None) -> Optional[BinaryIO]: pass

    @abstractmethod
    def findDocumentById(self, document_id: str) -> Optional[Document]: pass

    @abstractmethod
    def findDocumentsByOwner(self, owner_id: str) -> List[Document]: pass

    @abstractmethod
    def findAllDocuments(self) -> List[Document]: pass

    @abstractmethod
    def updateMetaData(self, document: Document) -> bool: pass

    @abstractmethod
    def update_content(self, modified_by: str, document_id: str, content: BinaryIO, size: int) -> bool: pass

    @abstractmethod
    def deleteDocument(self, user_id: str, document_id: str) -> bool: pass

    @abstractmethod
    def addVersion(self, document_id: str, version: Version) -> bool: pass

    @abstractmethod
    def getVersions(self, document_id: str) -> List[Version]: pass

    @abstractmethod
    def restoreVersion(self, document_id: str, version_number: int) -> bool: pass

    # Permission
    @abstractmethod
    def shareDocument(self, document_id: str, user_id: str, permissions: List[str]) -> bool: pass

    @abstractmethod
    def removeShareDocument(self, document_id: str, user_id: str, permissions: List[str]) -> bool: pass

    @abstractmethod
    def getPermissionsByDoc(self, document_id: str) -> List[Permission]: pass

    @abstractmethod
    def getPermissionsByUser(self, user_id: str) -> List[Permission]: pass

    @abstractmethod
    def getPermissionsByUserDoc(self, user_id: str, doc_id: str) -> Optional[Permission]: pass

    # Department
    @abstractmethod
    def saveDepartment(self, department: Department) -> bool: pass

    @abstractmethod
    def findDepartmentById(self, department_id: str) -> Optional[Department]: pass

    @abstractmethod
    def findAllDepartments(self) -> List[Department]: pass

    @abstractmethod
    def updateDepartment(self, department: Department) -> bool: pass

    @abstractmethod
    def deleteDepartment(self, department_id: str) -> bool: pass

    # ActivityLog
    @abstractmethod
    def saveActivitylog(self, log: ActivityLog) -> bool: pass

    @abstractmethod
    def findActivitylogById(self, log_id: str) -> Optional[ActivityLog]: pass

    @abstractmethod
    def findActivitylogsByUser(self, user_id: str) -> List[ActivityLog]: pass

    @abstractmethod
    def findActivitylogsByDocument(self, document_id: str) -> List[ActivityLog]: pass

    @abstractmethod
    def findAllActivitylogs(self) -> List[ActivityLog]: pass

    @abstractmethod
    def updateActivitylog(self, log: ActivityLog) -> bool: pass

    @abstractmethod
    def deleteActivitylog(self, log_id: str) -> bool: pass