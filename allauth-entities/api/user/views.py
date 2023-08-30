#from django.contrib.auth.models import Group

from rest_framework import viewsets
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

from django.db.models import F

from api.user.serializers import (
    UserSerializer,
   # GroupSerializer,
)

"""
ViewSets are used to marshall data from requests into a model 
and vice versa.
"""
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = get_user_model().objects.all().order_by("-date_joined") # All users
    
    
    # Get the EmailAddress objects ordered by 'created'
    email_addresses = EmailAddress.objects.filter(
        user__is_active=True
    ).order_by('-email')

    # Get the User objects based on the related EmailAddress objects
    user_ids = email_addresses.values_list('user', flat=True)
    users = get_user_model().objects.filter(id__in=user_ids).order_by('-date_joined')

    # Optionally, annotate users with their email creation date
    users_with_email_dates = users.annotate(email_created=F('emailaddress'))



    serializer_class = UserSerializer
   

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """

#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
    