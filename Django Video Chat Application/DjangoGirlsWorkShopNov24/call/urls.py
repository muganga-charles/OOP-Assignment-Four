from django.urls import path

from . import views

app_name = 'call'

urlpatterns = [
    path('', views.videocall, name='call'),
]
