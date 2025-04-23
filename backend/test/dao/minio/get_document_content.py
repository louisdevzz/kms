from dao.management_dao import ManagementDAO

dao = ManagementDAO()
content = dao.get_document_content("68008d7153021d034787621a")
print(content.read(12) if content else "No content")
