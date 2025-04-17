from backend.dao.management_dao import ManagementDAO

dao = ManagementDAO()

document_id = "680096a538a0c7035d0fdc9f"


doc = dao.findDocumentById(document_id)

print(doc)