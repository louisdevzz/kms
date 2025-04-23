from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from dao.permission_module.ipermission_dao import IPermissionDAO
from dao.permission_module.permission import Permission


class PermissionDAO(IPermissionDAO):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str):
        self.db = mongo_client[database_name]
        self.collection = self.db[collection_name]

    def save(self, permission: Permission) -> bool:
        per_dict = permission.dict()
        per_dict['_id'] = ObjectId(per_dict['permissionId'])
        del per_dict['permissionId']
        result = self.collection.insert_one(per_dict)
        return result.acknowledged

    def findByUser(self, userId: str) -> List[Permission]:
        pers = self.collection.find({"userId": userId})
        return [self._convert_per(per) for per in pers]

    def findByDoc(self, docId: str, session=None) -> List[Permission]:
        pers = self.collection.find({"docId": docId})
        return [self._convert_per(per) for per in pers]

    def findByUserDoc(self, userId: str, docId: str) -> Optional[Permission]:
        per = self.collection.find_one({"userId": userId, "docId": docId})
        return self._convert_per(per)

    def findAll(self) -> List[Permission]:
        pers = self.collection.find({})
        return [self._convert_per(per) for per in pers]

    def update(self, permission: Permission) -> bool:
        per_dict = permission.dict()
        permissionId = ObjectId(per_dict['permissionId'])
        del per_dict['permissionId']
        result = self.collection.update_one(
            {"_id": permissionId},
            {"$set": per_dict}
        )
        return result.modified_count > 0

    def delete(self, permissionId: str, session=None) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(permissionId)})
        return result.deleted_count > 0

    @staticmethod
    def _convert_per(doc: dict) -> Optional[Permission]:
        if doc:
            doc["permissionId"] = str(doc["_id"])
            del doc["_id"]
            return Permission(**doc)
        return None
