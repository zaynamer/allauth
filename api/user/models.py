
from django.db import models
from allauth.account.models import EmailAddress
import requests

class CustomUser(models.Model):

    
    def get_active_account_id(self):
        try:
            active_email = EmailAddress.objects.get(user=self, primary=True, verified=True)
            return active_email.id
        except EmailAddress.DoesNotExist:
            return None
        
    

class User(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def get_active_account_id(self):
        active_account_id = self.custom_user.get_active_account_id()
        return active_account_id