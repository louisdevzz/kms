from knowledge.knowledge_manager import KnowledgeManager

knowledge = KnowledgeManager()

doc_id = '68074eace1b9646e19590cc3'
user_id = '67fb3f6efe93f7fdc7ef0580'

isdeleted = knowledge.delete(deleted_by=user_id, document_id=doc_id)
print("isDeleted:", isdeleted)
