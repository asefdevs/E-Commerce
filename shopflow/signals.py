from accounts.models import CustomUser
from .models import Basket
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(user=instance)

