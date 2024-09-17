from typing import Any, List
from notification.NotificationStrategy import NotificationStrategy


class EmailNotification(NotificationStrategy):
    
    def __init__(self, emails: List[str]):
        self.email_list = emails

    def send_notification(self, data:Any):
        for email in self.email_list:
            print(f"Sending Email Notification to {email} :: Scraped Data Count - {data.scraped_count} , Updated Data Count - {data.updated_count}")