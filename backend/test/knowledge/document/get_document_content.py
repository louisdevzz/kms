from backend.knowledge.knowledge_manager import KnowledgeManager

knowledge = KnowledgeManager()

doc_id = "68073d697fe0de018f4d3f3c"
user_id = "67fb3f6efe93f7fdc7ef0580"

content = knowledge.get_content(document_id=doc_id, user_id=user_id)
if content:
    print("Content:", content.read(5))
else:
    print('No content found')
