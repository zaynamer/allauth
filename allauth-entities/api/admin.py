from django.contrib import admin
#from .account.models import Account
from .user.models import User as NephrolyticsUser

#from .user.models import Profile
from django.contrib.auth.admin import UserAdmin

# Define an inline admin descriptor for Tenancy
# which acts a bit like a singleton
class NephrolyticsUserInline(admin.StackedInline):
    model = NephrolyticsUser

# Define a new User admin
class AccountAdmin(admin.ModelAdmin):
    #list_display = ["first_name", "last_name", "username", "email"]
    inlines = [NephrolyticsUserInline]


# Re-register UserAdmin
#admin.site.unregister(User)
admin.site.register(NephrolyticsUser, UserAdmin)
#admin.site.register(Account)
