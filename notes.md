# Steps to Set Up
* pipenv shell
* pipenv install django
* pipenv install djangorestframework
* pip freeze > requirements.txt (To create requirements file and populate with dependencies.)
* django-admin startproject api (starts boilerplate Django setup)
* cd api
* django-admin startapp authapp

** Manage.py talks to api.settings.py **

* `pipenv install pylint --dev` (makes your life easier)
* Add 'authapp' to the api.settings.py in `INSTALLED_APPS = []` to link authapp folder to connect it to api project.
* Also add: rest_framework (this is so that our endpoints will work later)
* In api fold to start server run: python manage.py runserver
* Now you can see the running server on localhost:8000 or by using the local IP address in your browser.
* Add `ALLOWED_HOSTS = ['*']` to api.settings.py to allow all user to access API. You can add an URL or IP address as well to allow them access.
* `pipenv install autopep8 --dev` to help with formatting.
* Cd back out of api folder and run `pip freeze > requirements.txt` to update dependencies in requirements.txt.
* Back in api folder restart server run `python manage.py runserver`
* `python manage.py migrate` to make migrations
* In api.urls.py is where your endpoints are located. We are given /admin as default.
* In api folder, create an admin account (superuser) by running: python manage.py createsuperuser
* Create a new endpoint in api.urls.py that will connect endpoint and views.
* Create in api folder views.py
* Add the following to the new api.views.py file:
```
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
```
* Then add:
```
@api_view(['GET'])
def index(request):
  date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  message = 'Server is live, current time is'
  return Response(data=message + date, status= status.HTTP_200_OK)
```
* In api folder, add a 3rd party authentication package. Run: `pip install djoser`

** djoser adds useful vews that we can use to build our authentication sysem. **

* Cd back out of api folder and run pip freeze > requirements.txt to update dependencies in requirements.txt.
* Add `'djoser'` to the api.settings.py under `INSTALLED_APPS = []`.
* Create in authapp folder urls.py. https://djoser.readthedocs.io/en/latest/base_endpoints.html
* In authapp.urls.py add the following:
```
from django.urls import path, include
from authapp import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
```
* Add `'rest_framework.authtoken'` to the api.settings.py under `INSTALLED_APPS = []`.
* Underneath `DATABASES={}` in our api.settings.py, add our Rest Framework configurations:
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSIONS_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```
* python manage.py migrate to make migrations (Because we added djoser views and rest framework.)
* Go to url `localhost:8000/auth/users/` and create a new user. (`users/` is a built in view from djoser)
* Go to url `localhost:8000/auth/token/login` to login in and get user token. (`token/login` is a built in view from djoser)
* Feel free to add preset collections to postman so that you do not have to make each time to test endpoints. For login in postman, remember to set the key value paires under BODY and not PARAMS.
* `After REST_FRAMEWORK={}` in our api.settings.py, you can add:
```
DJOSER = {
    'LOGIN_FIELD': 'email'
}
```
* This changes login feild of username to email if you want to. We are going to exclude it in this setup.
* To create a custom user login, under authapp.models.py add:
```
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    # add fields you would to update in database # we only need username password is default
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.username
```
* Next we will create a serializer.py file in our authapp folder.
* Add the following to authapp.serializer.py:
```
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import *

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username']
```
* After `REST_FRAMEWORK={}` in our api.settings.py, you can add:
```
AUTH_USER_MODEL = 'authapp.User'
```
* After `AUTH_USER_MODEL={}` in our api.settings.py, you can add:
```
DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True, # make user type password twice pretty kewl
    'SERIALIZERS': {
        'user_create': 'authentication.serializers.UserCreateSerializer',
        'user': 'authentication.serializers.UserCreateSerializer',
        'current_user': 'authentication.serializers.CurrentUserSerializer'
    },
}
```
* Under authapp.views.py add the following:
```
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted(request, *args, **kwargs):
  return Response(data="Only for Logged in User", status= status.HTTP_200_OK)
```
* We are restricting user access to those who are logged in only (Have a valid token).
* Add ```path('restricted/', views.restricted)``` to authapp.urls.py
* There is a built in logout endpoint from djoser. To access it via postman, you must place the current valid token in your header section under key: value pair: ```Authorization : Token <your token goes here>``` Example: ```Authorization Token 7a150ac5a7b71d6f97ba58e56ed7791f4433dd68```
* Then under the endpoint `http://localhost:8000/auth/token/logout` make a POST request.

** For more information please see: https://github.com/awaismirza/django-rest-framework and https://www.youtube.com/watch?v=ddB83a4jKSY **