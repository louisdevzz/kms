from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
from dao.permission_module.ipermission import IPermission


class Permission(BaseModel, IPermission):
    permissionId: str = Field(default_factory=lambda: str(ObjectId()), description="Unique identifier")  # Auto-generated
    userId: str = Field(..., description="ID of the user_module with permissions")
    docId: str = Field(..., description="ID of the document_module being accessed")
    permissions: List[str] = Field(..., description="List of permission_module strings")

    def __init__(
            self,
            userId: str,
            docId: str,
            permissions: List[str],
            **kwargs
    ):
        super().__init__(
            userId=userId,
            docId=docId,
            permissions=permissions,
            **kwargs
        )

    def to_json(self) -> str:
        return self.model_dump_json()

    def remove_permissions(self, permissions_to_remove: List[str]) -> bool:
        original_length = len(self.permissions)
        self.permissions = [p for p in self.permissions if p not in permissions_to_remove]
        return len(self.permissions) < original_length

