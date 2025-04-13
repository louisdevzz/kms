from abc import ABC, abstractmethod
from typing import List


class IPermission(ABC):
    @abstractmethod
    def to_json(self) -> str: pass

    @abstractmethod
    def remove_permissions(self, permissions_to_remove: List[str]) -> bool: pass