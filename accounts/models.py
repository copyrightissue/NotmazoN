# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # add additional fields in here
    age = models.PositiveIntegerField(null=True, blank=True)
    # bio = models.TextField(max_length=500, blank=True)

    # def __str__(self):
    #     return self.username
