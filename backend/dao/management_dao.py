from typing import List, Optional, BinaryIO
from pymongo import MongoClient
from backend.dao.user_module.user import User
from backend.dao.user_module.user_dao import UserDAO
from backend.dao.document_module.document import Document, Version
from backend.dao.document_module.document_dao import DocumentDAO
from backend.dao.department_module.department import Department
from backend.dao.department_module.department_dao import DepartmentDAO
from backend.dao.activitylog_module.activitylog import ActivityLog
from backend.dao.activitylog_module.activitylogdao import ActivityLogDAO
from backend.dao.permission_module.permission import Permission
from backend.dao.permission_module.permission_dao import PermissionDAO
from backend.dao.minio_module.storage import MinIOStorage
from datetime import timedelta
from backend.utils.config_loader import get_storage_config, get_collections, get_db_config
from backend.dao.imanagement_dao import IManagementDAO


class ManagementDAO(IManagementDAO):
    def __init__(self):
        mongo_config = get_db_config()
        minio_config = get_storage_config()
        collects = get_collections()

        """single MongoDB connection"""
        self.mongo_client = MongoClient(mongo_config['uri'])
        self.database_name = mongo_config['db_name']

        # daos
        self.user_dao = UserDAO(self.mongo_client, self.database_name, collects['user_dao'])
        self.document_dao = DocumentDAO(self.mongo_client, self.database_name, collects['document_dao'])
        self.department_dao = DepartmentDAO(self.mongo_client, self.database_name, collects['department_dao'])
        self.activity_log_dao = ActivityLogDAO(self.mongo_client, self.database_name, collects['activity_log_dao'])
        self.permission_dao = PermissionDAO(self.mongo_client, self.database_name, collects['permission_dao'])

        # minio_module storage
        self._minio_storage = MinIOStorage(
            endpoint=minio_config['endpoint'],
            access_key=minio_config['access_key'],
            secret_key=minio_config['secret_key'],
            bucket_name=minio_config['bucket_name'],
            secure=minio_config.get('secure')
        )

    def close_connection(self):
        self.mongo_client.close()

    # User
    def saveUser(self, user: User) -> bool:
        return self.user_dao.save(user)

    def findUserById(self, user_id: str) -> Optional[User]:
        return self.user_dao.findById(user_id)

    def findUserByEmail(self, email: str) -> Optional[User]:
        return self.user_dao.findByEmail(email)

    def findAllUsers(self) -> List[User]:
        return self.user_dao.findAll()

    def updateUser(self, user: User) -> bool:
        return self.user_dao.update(user)

    def deleteUser(self, user_id: str) -> bool:
        return self.user_dao.delete(user_id)

    # Document
    def saveDocument(self, document: Document, content: Optional[BinaryIO] = None) -> dict:
        result = {}
        try:
            # save metadata to mongo
            if not self.document_dao.save(document):
                raise Exception("Failed to save document metadata to MongoDB")

            saved_doc = self.document_dao.findByName(name=document.name)

            # add all permissions for owner
            permission = Permission(
                userId=document.owner,
                docId=saved_doc.documentId,
                permissions=["read", "write", "share", "delete"]
            )
            if not self.permission_dao.save(permission):
                raise Exception("Failed to save permission to MongoDB")

            result['document'] = saved_doc

            # save content to Minio
            if content is not None:
                object_name = f"{document.documentId}/v{document.currentNumber}"

                if not self._minio_storage.addDoc(
                        object_name=object_name,
                        data=content,
                        length=document.size,
                        content_type=document.dType
                ):
                    # failed to store to minio --> drawback on mongo
                    self.document_dao.delete(document.documentId)
                    raise Exception("Failed to store content in Minio")

                result['content_url'] = self._minio_storage.getDocUrl(
                    object_name=object_name,
                    expires=timedelta(hours=24)
                )

        except Exception as e:
            if 'document' in result:
                self.document_dao.delete(document.documentId)

            if 'content_url' in result:
                object_name = f"{document.documentId}/v{document.currentNumber}"
                self._minio_storage.deleteDoc(object_name)

            result = {'error': str(e)}

        return result

    def get_document_content(self, document_id: str, version_num: Optional[int] = None) -> Optional[BinaryIO]:
        # get metadata
        document = self.findDocumentById(document_id)
        if not document:
            return None

        if version_num:
            version = next((v for v in document.versions
                            if v.version_number == version_num), None)
            if not version:
                return None
            object_name = f"{document_id}/v{version_num}"
        else:
            # latest version
            object_name = f"{document_id}/v{document.currentNumber}"

        return self._minio_storage.getDoc(object_name)

    def findDocumentById(self, document_id: str) -> Optional[Document]:
        return self.document_dao.findById(document_id)

    def findDocumentsByOwner(self, owner_id: str) -> List[Document]:
        return self.document_dao.findByOwner(owner_id)

    def findAllDocuments(self) -> List[Document]:
        return self.document_dao.findAll()

    def updateMetaData(self, document: Document) -> bool:
        return self.document_dao.updateMetaData(document)

    def update_content(self, modified_by: str, document_id: str, content: BinaryIO, size: int) -> bool:
        document = self.findDocumentById(document_id)
        if not document:
            return False
        document.set_version(modified_by, size)  # set version
        object_name = f"{document_id}/v{document.currentNumber}"
        return self._minio_storage.addDoc(object_name, content, size)

    def deleteDocument(self, document_id: str) -> bool:
        return self.document_dao.delete(document_id)

    def addVersion(self, document_id: str, version: Version) -> bool:
        return self.document_dao.addVersion(document_id, version)

    def getVersions(self, document_id: str) -> List[Version]:
        return self.document_dao.getVersions(document_id)

    def restoreVersion(self, document_id: str, version_number: int) -> bool:
        return self.document_dao.restoreVersion(document_id, version_number)

    # Permission
    def shareDocument(self, document_id: str, user_id: str, permissions: List[str]) -> bool:
        existing = self.permission_dao.findByDoc(document_id)
        for perm in existing:
            if perm.userID == user_id:
                # update
                perm.permissions = list(set(perm.permissions + permissions))
                return self.permission_dao.update(perm)

        permission = Permission(
            userID=user_id,
            docID=document_id,
            permissions=permissions
        )
        return self.permission_dao.save(permission)

    def removeShareDocument(self, document_id: str, user_id: str, permissions: List[str]) -> bool:
        try:
            user_permissions = self.getPermissionsByUserDoc(user_id, document_id)
            if not user_permissions:
                return False

            success = True
            if not user_permissions.remove_permissions(permissions):
                success = False

            return success
        except Exception:
            return False

    def getPermissionsByDoc(self, document_id: str) -> List[Permission]:
        return self.permission_dao.findByDoc(document_id)

    def getPermissionsByUser(self, user_id: str) -> List[Permission]:
        return self.permission_dao.findByUser(user_id)

    def getPermissionsByUserDoc(self, user_id: str, doc_id: str) -> Optional[Permission]:
        return self.permission_dao.findByUserDoc(user_id, doc_id)

    # Department
    def saveDepartment(self, department: Department) -> bool:
        return self.department_dao.save(department)

    def findDepartmentById(self, department_id: str) -> Optional[Department]:
        return self.department_dao.findById(department_id)

    def findAllDepartments(self) -> List[Department]:
        return self.department_dao.findAll()

    def updateDepartment(self, department: Department) -> bool:
        return self.department_dao.update(department)

    def deleteDepartment(self, department_id: str) -> bool:
        return self.department_dao.delete(department_id)

    # ActivityLog
    def saveActivitylog(self, log: ActivityLog) -> bool:
        return self.activity_log_dao.save(log)

    def findActivitylogById(self, log_id: str) -> Optional[ActivityLog]:
        return self.activity_log_dao.findById(log_id)

    def findActivitylogsByUser(self, user_id: str) -> List[ActivityLog]:
        return self.activity_log_dao.findByUser(user_id)

    def findActivitylogsByDocument(self, document_id: str) -> List[ActivityLog]:
        return self.activity_log_dao.findByDocument(document_id)

    def findAllActivitylogs(self) -> List[ActivityLog]:
        return self.activity_log_dao.findAll()

    def updateActivitylog(self, log: ActivityLog) -> bool:
        return self.activity_log_dao.update(log)

    def deleteActivitylog(self, log_id: str) -> bool:
        return self.activity_log_dao.delete(log_id)
