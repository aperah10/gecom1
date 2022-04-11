from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
import json 
from django.core import serializers


# automatic profile
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            upload=instance,
            id=instance.id,
            fullname=instance.fullname,)
        CartProfile.objects.create(id=instance.id,
            upload=instance, cartUpload={})


@receiver(post_save, sender=CartProduct)
def save_Cartprofile(sender, instance, created, **kwargs):
    if created:
        # print(instance)
        prodList = CartProduct.objects.filter(upload=instance.upload)
        tmpJson = serializers.serialize("json",prodList)
        tmpObj = json.loads(tmpJson)
        CartProfile.objects.update_or_create(
            upload=instance.upload, defaults= {'cartUpload':tmpObj })