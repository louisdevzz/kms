from abc import ABC, abstractmethod
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
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


class DocumentDAO(IDocumentDAO):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection: str):
        self.db = mongo_client[database_name]
        self.collection = self.db[collection]

    def save(self, document: Document) -> bool:
        doc_dict = document.dict()
        doc_dict["_id"] = ObjectId(doc_dict["documentId"])  # string to ObjectId
        del doc_dict["documentId"]
        result = self.collection.insert_one(doc_dict)
        return result.acknowledged

    def findById(self, documentId: str) -> Optional[Document]:
        doc = self.collection.find_one({"_id": ObjectId(documentId)})
        if doc:
            doc["documentId"] = str(doc["_id"])
            del doc["_id"]
            return Document(**doc)  # mongo_dict -> doc object
        return None

    def findByName(self, name: str) -> Optional[Document]:
        doc = self.collection.find_one({"name": name})
        return self._convert_doc(doc) if doc else None

    def findByOwner(self, ownerId: str) -> List[Document]:
        docs = self.collection.find({"owner": ObjectId(ownerId)})
        return [self._convert_doc(doc) for doc in docs]

    def findAll(self) -> List[Document]:
        docs = self.collection.find({})
        return [self._convert_doc(doc) for doc in docs]

    def updateMetaData(self, document: Document) -> bool:
        doc_dict = document.dict()
        document_id = ObjectId(doc_dict["documentId"])
        del doc_dict["documentId"]
        result = self.collection.update_one(
            {"_id": document_id}, {"$set": doc_dict}
        )
        return result.modified_count > 0

    def delete(self, documentId: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(documentId)})
        return result.deleted_count > 0

    def addVersion(self, documentId: str, version: Version) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(documentId)},
            {"$push": {"versions": version.dict()}}
        )
        return result.modified_count > 0

    def getVersions(self, documentId: str) -> List[Version]:
        doc = self.collection.find_one({"_id": ObjectId(documentId)}, {"versions": 1})  # only versions
        versions = doc.get("versions", []) if doc else []
        return [Version(**v) for v in versions]  # mongo_dict -> version object

    def restoreVersion(self, documentId: str, version_number: int) -> bool:
        doc = self.collection.find_one({"_id": ObjectId(documentId)}, {"versions": 1})
        if doc:
            for version in doc.get("versions", []):
                if version["version_number"] == version_number:
                    result = self.collection.update_one(
                        {"_id": ObjectId(documentId)},
                        {"$set": {"currentNumber": version_number}}
                    )
                    return result.modified_count > 0
        return False

    # mong_dict -> object
    @staticmethod
    def _convert_doc(doc: dict) -> Document:
        doc["documentId"] = str(doc["_id"])
        del doc["_id"]
        return Document(**doc)

