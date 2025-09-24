from rest_framework import serializers
from parking.models import CompanyArea,AreaMembership,Vechile,ParkingRatePlan
from parking.models import Company
from django.contrib.auth.models import User

class CompanyAreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    company = serializers.PrimaryKeyRelatedField(queryset = Company.objects.all(), required = True)

    class Meta:
        model = CompanyArea
        fields = '__all__'
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        return data


class CompanyAreaMemebershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required=True)
    class Meta:
        model= AreaMembership
        fields = '__all__'

class VechileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vechile
        fields = '__all__'


class ParkingAreaPlanSerializer(serializers.ModelSerializer):
    remaining_space = serializers.CharField(read_only=True)
    price = serializers.IntegerField(required=True)
    class Meta:
        model = ParkingRatePlan
        fields = '__all__'