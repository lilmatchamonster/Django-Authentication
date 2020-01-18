from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    # add fields you would to update in database # we only need username password is default
    REQUIRED_FIELDS = []

    def get_username(self):
        return self.username