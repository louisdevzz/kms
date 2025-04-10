from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.document_module.document import Document, Version

class IDocumentDAO(ABC):
    @abstractmethod
    def save(self, document: Document) -> bool: pass

    @abstractmethod
    def findById(self, documentId: str) -> Optional[Document]: pass

    @abstractmethod
    def findByName(self, name: str) -> Optional[Document]: pass

    @abstractmethod
    def findByOwner(self, ownerId: str) -> List[Document]: pass

    @abstractmethod
    def findAll(self) -> List[Document]: pass

    @abstractmethod
    def updateMetaData(self, document: Document) -> bool: pass

    @abstractmethod
    def delete(self, documentId: str) -> bool: pass

    @abstractmethod
    def addVersion(self, documentId: str, version: Version) -> bool: pass

    @abstractmethod
    def getVersions(self, documentId: str) -> List[Version]: pass

    @abstractmethod
    def restoreVersion(self, documentId: str, version_number: int) -> bool: pass