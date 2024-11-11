from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.

class Phone_user(AbstractUser):
    phone = models.CharField(max_length=10,unique=True)
    USERNAME_FIELD= 'phone'
    REQUIRED_FIELDS= []
    objects = UserManager()
    