import uuid

from django.db import models
from django.db.models.fields import UUIDField, EmailField, CharField, BooleanField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username = CharField(max_length=250, unique=True, db_index=True)

    def __str__(self):
        return self.username
