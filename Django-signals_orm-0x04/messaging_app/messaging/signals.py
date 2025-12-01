from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, User

# Task 0: Create notification when a new message is saved
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

# Task 1 (later): Log old content before edit
# Example placeholder for pre_save
# @receiver(pre_save, sender=Message)
# def log_message_edit(sender, instance, **kwargs):
#     if instance.pk:
#         old_message = Message.objects.get(pk=instance.pk)
#         if old_message.content != instance.content:
#             instance.edited = True
#             # Save old content into MessageHistory (to be defined)
