from django.db import models
from django.contrib.auth.models import User
from company.models import Company

# Create your models here.
class CompanyArea(models.Model):
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    name = models.CharField(max_length=60, null=True, blank= True, verbose_name="Area Name")
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} --> {self.company}'
    

class Role(models.IntegerChoices):
        MANAGER = 10, "Manager"
        WORKER = 20, "Worker"

class AreaMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null= True)
    area = models.ForeignKey(CompanyArea, on_delete=models.RESTRICT)
    role = models.IntegerField(choices= Role.choices)

    def __str__(self):
         return f'{self.area} -- {self.user.username}'
    
    class Meta:
        unique_together = ("user","area")
    
class Vechile(models.Model):

     
    name = models.CharField(max_length=50)

    def __str__(self):
          return self.name
     

class ParkingRatePlan(models.Model):
    name = models.ForeignKey(Company , on_delete= models.RESTRICT)
    area = models.ForeignKey(CompanyArea, on_delete=models.RESTRICT)
    vechile = models.ForeignKey(Vechile, on_delete=models.RESTRICT)
    no_of_space = models.PositiveIntegerField(default=0)
    remaining_space = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
          return f'{self.name}--{self.area.name}--{self.no_of_space}'
     
class BookingStatus(models.IntegerChoices):
    BOOK = 10, "Book"
    PARKING_IN = 20, "Parking_In"
    PARKING_OUT = 30, "Parking_Out"
    CANCEL = 40, "Cancel"
    COMPLETED = 50 ,"Completed"

class PaymentStatus(models.IntegerChoices):
    NONE =  50 , "None"
    INITIAL = 10 , "Initial"
    SUCCESS = 20, "Success"
    FAILED = 30 , "Failed"
    USER_CANCELED = 40 ,"User canceled"

class PaymentType(models.IntegerChoices):
    CASH = 10, "CASH"
    KHALTI = 20, "KHALTI"
    ESEWA = 30, "ESWEA"

class BookParking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    vechile = models.ForeignKey(Vechile, on_delete=models.RESTRICT)
    vechile_number = models.CharField(max_length=50, null= True, blank = True)
    area = models.ForeignKey(CompanyArea, on_delete=models.RESTRICT)
    per_hour_price = models.PositiveIntegerField(default=0)
    time_in = models.DateTimeField(null=True,blank=True)
    time_out = models.DateTimeField(null=True,blank=True)
    total_time = models.FloatField(null=True, blank=True)
    status = models.IntegerField(choices=BookingStatus.choices, default=BookingStatus.BOOK)
    amount = models.FloatField(null=True,blank=True)
    discount_amount = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    is_promocode_used = models.BooleanField(default=False)
    promocode = models.CharField(max_length=50, null= True, blank = True)
    payment_type = models.IntegerField(choices=PaymentType.choices, default=PaymentType.CASH)
    payment_status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.NONE)
    txn_id = models.CharField(max_length=50, null=True, blank=True)
    pidx = models.CharField(max_length=50, null=True, blank=True)

    
    def __str__(self):
        return f'{self.user}-{self.vechile_number} - {self.area}'