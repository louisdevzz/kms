from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from backend.dao.activitylog_module.iactivitylog import IActivityLog


class ActivityLog(BaseModel, IActivityLog):
    activityLogId: str = Field(default_factory=lambda: str(ObjectId()), description="Unique identifier")  # Auto-generated
    userId: str = Field(..., description="ID of the user_module who performed the action")
    docId: str = Field(..., description="ID of the document_module involved")
    action: str = Field(..., description="Type of action performed")
    description: str = Field(..., description="Detailed description of the activity")
    date: datetime = Field(..., description="Timestamp of the activity")

    def __init__(
            self,
            userId: str,
            docId: str,
            action: str,
            description: str,
            **kwargs
    ):
        super().__init__(
            userId=userId,
            docId=docId,
            action=action,
            description=description,
            date=datetime.now(),
            **kwargs
        )

    def to_json(self) -> str:
        return self.model_dump_json()

    def get_actor(self) -> str:
        return self.userId

    def get_action(self) -> str:
        return self.action

    def get_date(self) -> datetime:
        return self.date

    def get_description(self) -> str:
        return self.description
