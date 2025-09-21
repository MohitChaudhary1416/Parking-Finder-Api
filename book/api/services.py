import json
import os

import requests
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from parking.api.serializer import CompanyAreaSerializer
from parking.models import (BookingStatus, ParkingRatePlan, PaymentStatus, BookParking,
                            PaymentType)
from promocode.models import Promocode


class KhaltiServices:
    def __init__(self):
        self.authorization_key = os.getenv("KHALTI_KEY")

    def get_khalti_url(self, parking):
        url = "https://dev.khalti.com/api/v2/epayment/initiate/"
        payload = json.dumps(
            {
                "return_url": "http://localhost:8000/api/booking/callback_url",
                "website_url": "https://example.com/",
                "amount": parking.total_amount * 100,
                "purchase_order_id": parking.id,
                "purchase_order_name": f"{parking.area}- {parking.vechile} - {parking.vechile_number}",
                "customer_info": {
                    "name": parking.user.username,
                    "email": parking.user.email or '',
                    "phone": "",
                },
                "product_details": [
                    {
                        "identity": parking.id,
                        "name": f"{parking.area}- {parking.vechile} - {parking.vechile_number}",
                        "total_price": parking.total_amount * 100,
                        "quantity": 1,
                        "unit_price": parking.total_amount * 100,
                    }
                ],
            }
        )
        headers = {
            "Authorization": f"key {self.authorization_key}",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            parking.pidx = data['pidx']
            print("done")
            return data['payment_url']
        return ""


class BookParkingServices:
    def promocode(self, book_parking):
        promocode = Promocode.objects.get(name=book_parking.promocode)
        if promocode.remaining_to_use != 0:
            discount_amount = book_parking.total_amount * (promocode.discount / 100)
            book_parking.discount_amount = discount_amount
            book_parking.total_amount = book_parking.total_amount - discount_amount
            book_parking.is_promocode_used = True
            book_parking.save()
            promocode.remaining_to_use = promocode.remaining_to_use - 1
            promocode.save()

    def decrease_parking_space(self, parking_area):
        parking_area.remaining_space = parking_area.remaining_space - 1
        parking_area.save()

    def update_parking(self, parking):
        total_time = (timezone.now() - parking.time_in).total_seconds() / 3600
        if total_time <= 1:
            parking.total_time = 1
        else:
            parking.total_time = total_time
        parking.time_out = timezone.now()

        if total_time > 1 and parking.is_promocode_used == True:
            promocode = Promocode.objects.get(name=parking.promocode)
            amount = parking.per_hour_price * total_time
            discount_amount = amount * (promocode.discount / 100)
            total_amount = amount - discount_amount
            parking.amount = int(amount)
            parking.discount_amount = int(discount_amount)
            parking.total_amount = int(total_amount)

        elif total_time > 1:
            amount = parking.per_hour_price * total_time
            parking.amount = int(amount)
            parking.discount_amount = 0
            parking.total_amount = int(amount)
        if parking.payment_type not in [
            PaymentType.KHALTI.value,
            PaymentType.ESEWA.value,
        ]:
            parking.status = BookingStatus.COMPLETED
        else:
            parking.payment_status = PaymentStatus.INITIAL
            khalti = KhaltiServices()
            url = khalti.get_khalti_url(parking)
            parking.save()
            return {
                "payment_online":True,
                "url":url
            }
        parking.save()
        return {
            "payment_online":False,
            "url":""
        }