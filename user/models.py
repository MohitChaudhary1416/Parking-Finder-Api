from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name= 'userdetail')
    is_kyc_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True,blank=True)
    citizenship_number = models.CharField(null=True,blank=True)
    citizenship_image = models.ImageField(upload_to='citizenship', null=True, blank= True)

    def __str__(self):
        return self.user.username