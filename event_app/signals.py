from .models import Event,Asset
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
import os

# @receiver(post_save,sender=Event)
# def create_asset(sender,instance,created,**kwargs):
#     if created:
#         Asset.objects.create(event=instance)


@receiver(pre_save, sender=Asset)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.id:
        return 
    try:
        old_image = Asset.objects.get(id=instance.id).event_image
    except Event.DoesNotExist:
        return 

    new_image = instance.event_image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=Asset)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.event_image and os.path.isfile(instance.event_image.path):
        os.remove(instance.event_image.path)