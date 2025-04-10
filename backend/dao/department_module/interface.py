from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from bson import ObjectId


class IDepartment(ABC):
    @abstractmethod
    def to_json(self) -> str: pass

    @abstractmethod
    def get_name(self) -> str: pass

    @abstractmethod
    def get_description(self) -> str: pass

    @abstractmethod
    def set_name(self, new_name: str) -> bool: pass

    @abstractmethod
    def set_description(self, new_description: str) -> bool: pass