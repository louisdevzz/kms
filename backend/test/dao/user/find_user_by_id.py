import unittest
import mongomock
from backend.dao.management_dao import ManagementDAO
from backend.dao.user_module.user import User


class FindUserById(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mongo_client = mongomock.MongoClient()
        cls.database = cls.mongo_client['testdb']
        cls.dao = ManagementDAO(cls.mongo_client, cls.database)

    def test_find_user_by_id_valid(self):
        user = User(
            name="Alice Smith",
            email="alice@example.com",
            password="hashed_pw",
            departmentId="finance",
            roles=["manager"]
        )
        # save user first
        self.dao.saveUser(user)
        user_id = str(user.userId)

        # find
        found_user = self.dao.findUserById(user_id)

        if found_user:
            print(f"\n✅ Found user: {found_user.name}")
        else:
            print("❌ User not found.")
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, "alice@example.com")

    def test_find_user_by_id_invalid(self):
        fake_id = "000000000000000000000000"
        found_user = self.dao.findUserById(fake_id)

        if found_user is None:
            print("\n✅ Correctly returned None for nonexistent user.")
        else:
            print("❌ Expected None, but found a user.")
        self.assertIsNone(found_user)


if __name__ == '__main__':
    unittest.main()
