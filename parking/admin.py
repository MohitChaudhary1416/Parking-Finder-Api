from django.contrib import admin
from parking.models import CompanyArea,AreaMembership,Vechile,ParkingRatePlan,BookParking

# Register your models here.
@admin.register(CompanyArea)
class CompanyAreaAdmin(admin.ModelAdmin):
    list_display = ['id','company','name','rating','company__owner']

@admin.register(AreaMembership)
class AreamembershipAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'area', 'role']

@admin.register(Vechile)
class VechileAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ParkingRatePlan)
class ParkingRatePlanAdmin(admin.ModelAdmin):
    list_display = ['name','area','vechile','no_of_space','price','remaining_space']

@admin.register(BookParking)
class BookparkingAdmin(admin.ModelAdmin):
    list_display = ['user','vechile','vechile_number','area','status','total_amount']





