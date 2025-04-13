from backend.dao.user_module.iuser_dao import IUserDAO
from backend.dao.user_module.user import User
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional


class UserDAO(IUserDAO):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection: str):
        self.db = mongo_client[database_name]
        self.collection = self.db[collection]

    def save(self, user: User) -> bool:
        user_dict = user.dict()
        user_dict["_id"] = ObjectId(user_dict["userId"])  # Convert to ObjectId
        del user_dict["userId"]
        result = self.collection.insert_one(user_dict)
        return result.acknowledged

    def findById(self, userId: str) -> Optional[User]:
        user = self.collection.find_one({"_id": ObjectId(userId)})
        if user:
            return self._convert_doc(user)
        return None

    def findByEmail(self, email: str) -> Optional[User]:
        user = self.collection.find_one({"email": email})
        if user:
            return self._convert_doc(user)
        return None

    def findAll(self) -> List[User]:
        users = self.collection.find({})
        return [self._convert_doc(user) for user in users]

    def update(self, user: User) -> bool:
        user_dict = user.dict()
        user_id = ObjectId(user_dict["userId"])
        del user_dict["userId"]
        result = self.collection.update_one(
            {"_id": user_id},
            {"$set": user_dict}
        )
        return result.modified_count > 0

    def delete(self, userId: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(userId)})
        return result.deleted_count > 0

    @staticmethod
    def _convert_doc(doc: dict) -> User:
        doc["userId"] = str(doc["_id"])
        del doc["_id"]
        return User(**doc)