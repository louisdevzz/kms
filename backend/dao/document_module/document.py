from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from dao.document_module.idocument import IDocument


class Version(BaseModel):
    version_number: int = Field(..., description="The version number of the document")
    modified_by: str = Field(..., description="User ID who modified this version")
    modification_date: datetime = Field(..., description="Date and time of modification")
    file_size: int = Field(..., description="Size of the file in bytes")


class Document(BaseModel, IDocument):
    documentId: str = Field(default_factory=lambda: str(ObjectId()), description="Unique identifier for the document")
    name: str = Field(..., description="Title or name of the document")
    owner: str = Field(..., description="Reference to the User who uploaded the document")
    dType: str = Field(..., description="File type (e.g., PDF, DOCX, JPEG)")
    departmentId: str = Field(..., description="Reference to Departments collection")
    tags: List[str] = Field([], description="Keywords describing the document content")
    category: str = Field(..., description="Broad categorization of the document")
    description: str = Field(..., description="Brief description of the document contents")
    university: str = Field(..., description="University associated with the document")
    additional: Optional[Dict] = Field(None, description="Extra metadata")
    currentNumber: int = Field(1, description="Current version number")
    versions: List[Version] = Field([], description="Version history")

    def __init__(
            self,
            name: str,
            owner: str,
            dType: str,
            departmentId: str,
            description: str,
            university: str,
            file_size: int,
            currentNumber: int = 1,
            tags: List[str] = None,
            category: str = None,
            additional: Optional[Dict] = None,
            **kwargs
    ):
        initial_version = Version(
            version_number=1,
            modified_by=owner,
            modification_date=kwargs.get('modification_date', datetime.now()),
            file_size=file_size
        )

        super().__init__(
            name=name,
            owner=owner,
            dType=dType,
            departmentId=departmentId,
            description=description,
            university=university,
            currentNumber=currentNumber,
            tags=tags,
            category=category,
            additional=additional,
            versions=[initial_version],
            **kwargs
        )

    def to_json(self) -> str:
        return self.model_dump_json()

    def get_dType(self) -> str:
        return self.dType

    def get_owner(self) -> str:
        return self.owner

    def get_department_id(self) -> str:
        return self.departmentId

    def get_university(self) -> str:
        return self.university

    def get_current_number(self) -> str:
        return self.currentNumber

    def set_owner(self, new_owner: str) -> bool:
        if new_owner:
            self.owner = new_owner
            return True
        return False

    def set_department(self, new_department: str) -> bool:
        if new_department:
            self.departmentId = new_department
            return True
        return False

    def set_university(self, new_university: str) -> bool:
        if new_university:
            self.university = new_university
            return True
        return False

    def set_current_version_number(self, new_version_number: int) -> bool:
        if new_version_number > 0:
            self.currentNumber = new_version_number
            return True
        return False

    def set_version(self, modified_by: str, file_size: int) -> bool:
        new_version_number = self.set_current_version_number(self.currentNumber + 1)
        new_version = Version(
            version_number=new_version_number,
            modified_by=modified_by,
            modification_date=datetime.now(),
            size=file_size
        )
        self.versions.append(new_version)

        return True
