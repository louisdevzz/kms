from abc import ABC, abstractmethod
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from backend.dao.activitylog_module.activitylog import ActivityLog


class IActivityLogDAO(ABC):
    @abstractmethod
    def save(self, log: ActivityLog) -> bool: pass

    @abstractmethod
    def findById(self, activityLogId: str) -> Optional[ActivityLog]: pass

    @abstractmethod
    def findByUser(self, userId: str) -> List[ActivityLog]: pass

    @abstractmethod
    def findByDocument(self, docId: str) -> List[ActivityLog]: pass

    @abstractmethod
    def findAll(self) -> List[ActivityLog]: pass

    @abstractmethod
    def update(self, log: ActivityLog) -> bool: pass

    @abstractmethod
    def delete(self, activityLogId: str) -> bool: pass


class ActivityLogDAO(IActivityLogDAO):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str):
        self.db = mongo_client[database_name]
        self.collection = self.db[collection_name]

    def save(self, log: ActivityLog) -> bool:
        log_dict = log.dict()
        log_dict['_id'] = ObjectId(log_dict['activityLogId'])
        del log_dict['activityLogId']
        result = self.collection.insert_one(log_dict)
        return result.acknowledged

    def findById(self, activityLogId: str) -> Optional[ActivityLog]:
        log = self.collection.find_one({"_id": ObjectId(activityLogId)})
        return self._convert_log(log) if log else None

    def findByUser(self, userId: str) -> List[ActivityLog]:
        logs = self.collection.find({"userId": userId})
        return [self._convert_log(log) for log in logs]

    def findByDocument(self, docId: str) -> List[ActivityLog]:
        logs = self.collection.find({"docId": docId})
        return [self._convert_log(log) for log in logs]

    def findAll(self) -> List[ActivityLog]:
        logs = self.collection.find({})
        return [self._convert_log(log) for log in logs]

    def update(self, log: ActivityLog) -> bool:
        log_dict = log.dict()
        log_id = ObjectId(log_dict['activityLogId'])
        del log_dict['activityLogId']
        result = self.collection.update_one(
            {"_id": log_id},
            {"$set": log_dict}
        )
        return result.modified_count > 0

    def delete(self, activityLogId: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(activityLogId)})
        return result.deleted_count > 0

    @staticmethod
    def _convert_log(log: dict) -> Optional[ActivityLog]:
        if log:
            log["activityLogId"] = str(log["_id"])
            del log["_id"]
            return ActivityLog(**log)
        return None