from django.db import models
from ..users.models import User


class NotificationMessage(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    linkback = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        # managed = False
        db_table = 'cms_notification_messages'
        ordering = ['-timestamp']


class Notification(models.Model):
    message = models.ForeignKey(NotificationMessage, related_name='messages', null=True, blank=True, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        # managed = False
        db_table = 'cms_notifications'
