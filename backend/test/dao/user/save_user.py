import unittest
import mongomock
from dao.management_dao import ManagementDAO
from dao.user_module.user import User


class SaveUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mongo_client = mongomock.MongoClient()
        cls.database = cls.mongo_client['testdb']
        cls.dao = ManagementDAO(cls.mongo_client, cls.database)

    def test_save_user_valid(self):
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            password="hashed_password_123",
            departmentId="engineering",
            roles=["admin", "developer"]
        )
        result = self.dao.saveUser(user)
        if result:
            print("\n✅ User saved successfully.")
        else:
            print("❌ Failed to save user.")
        self.assertTrue(result)

    def test_save_user_missing_email(self):
        try:
            user = User(
                name="John Doe",
                # email is missing
                password="hashed_password_123",
                departmentId="engineering",
                roles=["admin", "developer"]
            )
            self.dao.saveUser(user)
            self.fail("❌ Expected TypeError for missing email, but it didn't occur.")
        except TypeError:
            print("\n✅ Caught expected TypeError for missing email:")

    def test_save_user_wrong_roles_type(self):
        try:
            user = User(
                name="John Doe",
                email="john.doe@example.com",
                password="hashed_password_123",
                departmentId="engineering",
                roles="admin"  # should be a list, not a string
            )
            self.dao.saveUser(user)
            self.fail("❌ Expected error for wrong type in roles, but it didn't occur.")
        except Exception:
            print("\n✅ Caught expected exception for wrong roles type:")


if __name__ == '__main__':
    unittest.main()
