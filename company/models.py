from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null= True)
    address = models.CharField(max_length=100, blank= True, null = True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return self.name