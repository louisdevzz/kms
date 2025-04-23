from backend.dao.management_dao import ManagementDAO
dao = ManagementDAO()

object_names = [
]

for object_name in object_names:
    isDeleted = dao.deleteDoc(object_name)
    print(isDeleted)
