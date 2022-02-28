from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customers(User):
    phone=models.CharField(max_length=12,default="")
    gender=models.CharField(max_length=15,default="")
    address=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.username
    