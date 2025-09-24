from rest_framework import serializers
from company.models import Company
from datetime import datetime
class CompanySerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True)
    class Meta:
        model = Company
        fields = '__all__'
        

    def to_representation(self, instance):

        data =  super().to_representation(instance)
        data['time']=str(datetime.now())
        data['owner']=instance.owner.username  
        return data


class CompanyHyperSerialzier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['id','url','name']