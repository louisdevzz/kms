from abc import ABC, abstractmethod
from typing import List, Optional
from backend.dao.activitylog_module.activitylog import ActivityLog


class IActivityLogDAO(ABC):
    @abstractmethod
    def save(self, log: ActivityLog, session=None) -> bool: pass

    @abstractmethod
    def findById(self, activityLogId: str) -> Optional[ActivityLog]: pass

    @abstractmethod
    def findByUser(self, userId: str) -> List[ActivityLog]: pass

    @abstractmethod
    def findByDocument(self, docId: str) -> List[ActivityLog]: pass

    @abstractmethod
    def findAll(self) -> List[ActivityLog]: pass

    @abstractmethod
    def update(self, log: ActivityLog) -> bool: pass

    @abstractmethod
    def delete(self, activityLogId: str) -> bool: pass