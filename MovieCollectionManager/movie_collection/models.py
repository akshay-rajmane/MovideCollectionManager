from django.db import models
from django.db.models.fields import UUIDField, EmailField, CharField, BooleanField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username = CharField(max_length=250, unique=True, db_index=True)
    email = EmailField(unique=True, primary_key=True, db_index=True)
    uuid = UUIDField(unique=True, db_index=True)
    is_deleted = BooleanField(default=False)
    def __str__(self):
        return self.username
