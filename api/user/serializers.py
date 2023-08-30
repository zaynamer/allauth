from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

class UserSerializer(serializers.ModelSerializer):
    active_account_id = serializers.SerializerMethodField()

    def get_active_account_id(self, obj):
        try:
            active_email = EmailAddress.objects.get(user=obj, primary=True, verified=True)
            return active_email.id
        except EmailAddress.DoesNotExist:
            return None

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'groups', 'active_account_id']

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['id', 'name']



# from rest_framework import serializers
# from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'email', 'groups', 'accounts', 'active_account_id']

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['id', 'name']