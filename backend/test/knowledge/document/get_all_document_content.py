from backend.knowledge.knowledge_manager import KnowledgeManager

knowledge = KnowledgeManager()

user_id = "vohuunhan1310@gmail.com"

content = knowledge.get_all_content(user_id=user_id)
print("Content:", content)
