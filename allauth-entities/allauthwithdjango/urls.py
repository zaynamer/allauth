"""
URL configuration for allauthwithdjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404
from sampleapp import views as sampleappview
from . import views



# Configure the handler404 view
handler404 = sampleappview.custom_page_not_found




from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
#from api.account.views import AccountViewSet
from api.user.views import UserViewSet#, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,basename='User')
#router.register(r'groups', GroupViewSet)
#router.register(r'accounts', AccountViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),
    path('', include('sampleapp.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   
]