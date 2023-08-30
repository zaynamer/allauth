from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress

@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='GoogleUsers')
        instance.groups.add(group)
post_save.connect(assign_user_to_group, sender=User)
