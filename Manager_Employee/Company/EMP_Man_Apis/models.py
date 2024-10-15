from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.core.validators import MaxValueValidator, MinValueValidator

class Manager(AbstractUser):
    pass

class Employee(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField(validators=[MaxValueValidator(55), MinValueValidator(18)])
    designation = models.CharField(max_length=150,default='employee')
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    profile_img =models.ImageField(upload_to='employee_profile/', null=True, blank=True)
