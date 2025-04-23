from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from dao.department_module.idepartment_dao import IDepartmentDAO
from dao.department_module.department import Department


class DepartmentDAO(IDepartmentDAO):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str):
        self.db = mongo_client[database_name]
        self.collection = self.db[collection_name]

    def save(self, department: Department) -> bool:
        dept_dict = department.dict()
        dept_dict["_id"] = ObjectId(dept_dict["departmentId"])
        del dept_dict["departmentId"]
        result = self.collection.insert_one(dept_dict)
        return result.acknowledged

    def findById(self, departmentId: str) -> Optional[Department]:
        doc = self.collection.find_one({"_id": ObjectId(departmentId)})
        if doc:
            return self._convert_dept(doc)
        return None

    def findAll(self) -> List[Department]:
        docs = self.collection.find({})
        return [self._convert_dept(doc) for doc in docs]

    def update(self, department: Department) -> bool:
        dept_dict = department.dict()
        departmentId = ObjectId(dept_dict["departmentId"])
        del dept_dict["departmentId"]
        result = self.collection.update_one(
            {"_id": departmentId},
            {"$set": dept_dict}
        )
        return result.modified_count > 0

    def delete(self, departmentId: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(departmentId)})
        return result.deleted_count > 0

    @staticmethod
    def _convert_dept(doc: dict) -> Optional[Department]:
        if doc:
            doc["departmentId"] = str(doc["_id"])
            del doc["_id"]
            return Department(**doc)
        return None

