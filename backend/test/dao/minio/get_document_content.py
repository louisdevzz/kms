from backend.dao.management_dao import ManagementDAO

dao = ManagementDAO()
content = dao.get_document_content("67ff6896f9ff7650461d5b09")
print(content.read() if content else "No content")
