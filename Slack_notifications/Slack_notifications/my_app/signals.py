from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .utils import send_slack_notification

@receiver(post_save, sender=User)
def send_slack_notification_on_registration(sender, instance, created, **kwargs):
    if created:
        user_data = {
            "name": instance.username,
            "email": instance.email,
        }
        send_slack_notification(user_data)
