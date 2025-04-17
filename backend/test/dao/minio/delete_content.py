from backend.dao.management_dao import ManagementDAO
dao = ManagementDAO()

a = ['68007b7ce046bc82089924e9/v1', '68007cb4e046bc82089924ef/v1', '67ff6896f9ff7650461d5b09/v1', '68007c49e046bc82089924ec/v1']

isDeleted = dao.deleteDoc(a[0])
print(isDeleted)
