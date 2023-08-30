from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
@receiver(user_signed_up)
def assign_user_to_group(sender, request, user, **kwargs):
    group, created = Group.objects.get_or_create(name='GoogleUsers')
    user.groups.add(group)
    user.save()
    
    

class MyModel(models.Model):
    # Fields for your model

    class Meta:
        permissions = [
            ("can_create_sampleapp_entry", "Can create sampleapp entries"),
            ("can_view_sampleapp_entries", "Can view one or all entries"),
            # Add more custom permissions as needed
        ]

