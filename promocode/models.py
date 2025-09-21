from django.db import models
from parking.models import CompanyArea
class Promocode(models.Model):
    name = models.CharField(max_length=6, unique=True)
    area = models.ForeignKey(CompanyArea, on_delete=models.SET_NULL, null=True)
    to_use = models.PositiveIntegerField(default=10)
    remaining_to_use = models.PositiveIntegerField(default=0)
    discount = models.FloatField(default=0)