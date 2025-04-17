from backend.knowledge.knowledge_manager import KnowledgeManager

knowledge = KnowledgeManager()

user_id = "vohuunhan1310@gmail.com"

docIds = knowledge._perms.get_docId_by_userId(user_id=user_id)
print("docIds:", docIds)
