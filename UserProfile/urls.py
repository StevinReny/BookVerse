from django.urls import path

from UserProfile.views import CreateUser


urlpatterns=[path('create/',CreateUser.as_view(),name='create-user')]