from django.urls import path
from . import views

urlpatterns = [
    path('sampleapp/', views.sampleview, name='sampleapp'),
]