from dao.management_dao import ManagementDAO

dao = ManagementDAO()

document_id = "6807427cdb2b1ef4d5056c18"


doc = dao.findDocumentById(document_id)

print(doc)