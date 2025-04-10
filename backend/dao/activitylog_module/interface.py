from abc import ABC, abstractmethod
from datetime import datetime

class IActivityLog(ABC):
    @abstractmethod
    def to_json(self) -> str: pass

    @abstractmethod
    def get_actor(self) -> str: pass

    @abstractmethod
    def get_action(self) -> str: pass

    @abstractmethod
    def get_date(self) -> datetime: pass

    @abstractmethod
    def get_description(self) -> str: pass