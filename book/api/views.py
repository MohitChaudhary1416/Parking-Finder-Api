
from urllib import request

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from book.api.serializer import BookParkingSerializer, UpdateBookingSerializer,RatingSerialzier
from book.api.services import BookParkingServices
from company.models import Company
from parking.models import (AreaMembership, BookingStatus,BookParking,
                            CompanyArea, ParkingRatePlan, PaymentStatus, PaymentType, Vechile)
from rest_framework.decorators import api_view


class BookParkingView(GenericAPIView):
    serializer_class = BookParkingSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self,request,*args, **kwargs):
        data = request.data
        # serializer = self.get_serializer_class(data)
        serializer = BookParkingSerializer(data=data)
        if serializer.is_valid():
            book = serializer.save()
            parking_area = ParkingRatePlan.objects.get(
                area =book.area,
                vechile = book.vechile
            )
            book.user = request.user
            book.per_hour_price = parking_area.price
            book.amount = parking_area.price
            book.amount = parking_area.price
            book.time_in =timezone.now()
            book.total_amount = book.amount
            BookParkingServices.promocode(self,book)
            BookParkingServices.decrease_parking_space(self,parking_area)
            book.save()

            return Response({
                "message":"Booking successfully",
                "data":serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BookParkingUpdateView(GenericAPIView):

    def put(self,request, id, *args, **kwargs):
        data = request.data
        parking = BookParking.objects.get(id=id)
        if parking.status == BookingStatus.COMPLETED:
            return Response({
                "message":"Vechile is already parked out from this area"
            }, status.HTTP_400_BAD_REQUEST)

        if data['status'] == BookingStatus.BOOK:
            return Response({
                "message":"You cannot change status into book"
            }, status.HTTP_400_BAD_REQUEST)
        serializer = UpdateBookingSerializer(data=data, instance = parking)
        if serializer.is_valid():
            parking = serializer.save()
            if parking.status == BookingStatus.PARKING_OUT:
                data = BookParkingServices.update_parking(self,parking)
                if data['payment_online']:
                    return Response({
                        "message":"Book parking updated successfully",
                        "url":data['url'],
                        "data":serializer.data
                })
                else:
                    return Response({
                        "message":"Book parking updated successfully",
                        "data":serializer.data
                    })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



@api_view(['GET'])
def khalti_callback(request):
    payment = request.GET
    parking = BookParking.objects.get(pidx = payment['pidx'])
    status = payment['status']
    if status == "Completed":
        parking.status = BookingStatus.COMPLETED
        parking.txn_id = payment.get('transaction_id')
        parking.payment_status = PaymentStatus.SUCCESS
        parking.payment_type = PaymentType.KHALTI
    elif status == "User canceled":
        parking.payment_status = PaymentStatus.USER_CANCELED
        parking.payment_type = PaymentType.KHALTI
    else:
        parking.payment_status = PaymentStatus.FAILED
        parking.payment_type = PaymentType.KHALTI
    parking.save()



    return Response({
        "message":"Transaction completed"
    })



class BookingRatingView(GenericAPIView):

    @transaction.atomic
    def post(self,request, *args, **kwargs):
        data= request.data
        serialzier = RatingSerialzier(data=data)
        if serialzier.is_valid():
            booking = BookParking.objects.get(id=data['booking'])
            if booking.status != BookingStatus.COMPLETED:
                return Response({
                    "message":"Booking is not compeleted yet"
                },status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            rating = Rating.objects.filter(
                booking= data['booking']
            )
            if rating:
                return Response({
                    "message":"Rating is already provided"
                },status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            book_rating = serialzier.save()
            book_rating.user = request.user
            book_rating.save()
            company_area_rating = booking.area
            if company_area_rating.rating == 0:
                company_area_rating.rating = data['rating']
            else:
                company_area_rating.rating = (company_area_rating.rating + data['rating'])/2
            company_area_rating.save()
            return Response({
                "message":"Rating Completed"
            },status=status.HTTP_200_OK)
        return Response(serialzier.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)