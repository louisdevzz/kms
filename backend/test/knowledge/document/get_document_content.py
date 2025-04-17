from backend.knowledge.knowledge_manager import KnowledgeManager

knowledge = KnowledgeManager()

doc_id = "67ff6896f9ff7650461d5b09"
user_id = "vohuunhan1310@gmail.com"

content = knowledge.get_content(document_id=doc_id, user_id=user_id)
print("Content:", content.read(5))
