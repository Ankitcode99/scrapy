from abc import ABC, abstractmethod
from typing import Any

class NotificationStrategy(ABC):

    @abstractmethod
    def send_notification(self, data:Any):
        pass