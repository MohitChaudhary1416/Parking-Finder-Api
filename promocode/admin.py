from django.contrib import admin
from .models import Promocode
# Register your models here.
@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = [
        'area',
        'name',
        'to_use'
    ]