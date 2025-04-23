from backend.knowledge.knowledge_manager import KnowledgeManager

knowledge = KnowledgeManager()

name = "Test Text Document"
user_id = "67fb3f6efe93f7fdc7ef0580"

docs = knowledge.get_doc_by_name(name=name, user_id=user_id)
print("Content:", docs)
