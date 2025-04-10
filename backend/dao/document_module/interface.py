from abc import ABC, abstractmethod

class IDocument(ABC):
    @abstractmethod
    def to_json(self) -> str: pass

    @abstractmethod
    def get_dType(self) -> str: pass

    @abstractmethod
    def get_owner(self) -> str: pass

    @abstractmethod
    def get_department_id(self) -> str: pass

    @abstractmethod
    def get_university(self) -> str: pass

    @abstractmethod
    def set_owner(self, new_owner: str) -> bool: pass

    @abstractmethod
    def set_department(self, new_department: str) -> bool: pass

    @abstractmethod
    def set_university(self, new_university: str) -> bool: pass

    @abstractmethod
    def set_current_version_number(self, new_version_number: int) -> bool: pass

    @abstractmethod
    def set_version(self, modified_by: str, file_size: int) -> bool: pass