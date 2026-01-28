from django.dispatch import receiver
from django.contrib.auth.models import Group

from django.db.models.signals import post_save
from UserProfile.models import User


@receiver(post_save,sender=User)
def admin_to_group(sender,instance,created,**kwargs):
    if instance.role=='admin':
        admin_group,_=Group.objects.get_or_create(name="Admin")
        instance.groups.add(admin_group)
