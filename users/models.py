from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    avatar = models.ImageField(blank=True)
    gender = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=2, blank=True)
    currency = models.CharField(max_length=3, blank=True)
    superhost = models.BooleanField(default=False)
    login_method = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'