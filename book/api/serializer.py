from rest_framework import serializers

from parking.models import BookParking,CompanyArea, ParkingRatePlan, Vechile, BookingStatus
from rest_framework.exceptions import ValidationError

from promocode.models import Promocode


class BookParkingSerializer(serializers.ModelSerializer):
    per_hour_price = serializers.IntegerField(read_only=True)
    time_in = serializers.DateTimeField(read_only=True)
    time_out = serializers.DateTimeField(read_only=True)
    total_time = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    amount = serializers.FloatField(read_only=True)
    discount_amount = serializers.FloatField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)
    is_promocode_used = serializers.BooleanField(read_only=True)
    vechile_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    area = serializers.PrimaryKeyRelatedField(queryset=CompanyArea.objects.all(), required=True)
    vechile = serializers.PrimaryKeyRelatedField(queryset=Vechile.objects.all(), required=True)


    class Meta:
        model = BookParking
        fields = '__all__'

    # def validate(self, attrs):
    #     return super().validate(attrs)
    def validate_area(self, area):
        vechile = self.initial_data.get('vechile') 

        data = ParkingRatePlan.objects.filter(
            area=area,
            vechile_id=vechile
        ).first()

        if not data:
            raise ValidationError("You cannot book this vehicle in this area")

        if data.remaining_space <= 0:
            raise ValidationError("There is no space left for parking")

        return area



    # def validate_area(self, area):
    #     vechile = self.initial_data.get('vechile')
    #     data = ParkingRatePlan.objects.filter(
    #         area =area,
    #         vechile_id = vechile
    #     )

        # if data.first().remaining_space == 0:
        #     raise ValidationError("There is no space left for parking")

        # if data:
        #     return area
        # raise ValidationError("You cannot book this vechile in this area")

    def validate_promocode(self, promocode):
        data = Promocode.objects.filter(
            area = self.initial_data.get("area"),
            name = promocode
        )
        if data:
            return promocode
        raise ValidationError("Promocode doesnot exists")

    def validate_vehicle_number(self, vechile_number):
        parking = BookParking.objects.filter(
            area = self.initial_data.get('area'),
            vechile_number=vechile_number,
        ).exclude(
            status = BookingStatus.COMPLETED
        )
        if parking:
            raise ValidationError(f'{vechile_number} vehicle_number  already at parking area')
        return vechile_number



class UpdateBookingSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=True)
    payment_type = serializers.IntegerField(required=True)
    class Meta:
        model = BookParking
        fields = ['status','payment_type']