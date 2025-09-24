from django.db import models
from django.contrib.auth.models import User

from parking.models import BookParking


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    booking = models.ForeignKey(BookParking, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField()
    message = models.TextField(null=True)