from company.models import Company
from company.api.serializer import CompanySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET'])
def companylist(request):
    data = Company.objects.all()
    serializer = CompanySerializer(data, many = True)
    return Response(serializer.data,status.HTTP_200_OK)

@api_view(['POST'])
def createcompany(request):
    data = request.data
    serializer = CompanySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "Message":"Company Create Sucessfully"
        }, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['PUT'])
def update_company(request):
    data = request.data
    # company = Company.objects.get(id=id)
    company = get_object_or_404(Company, id=id)
    serializer = CompanySerializer(data=data, instance = company)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "Message":"Company Updated Sucessfully"
        }, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['DELETE'])
def delete_company(request):
    company = get_object_or_404(id=id)
    referenced = Company._meta.related_objects
    is_referenced = False
    for i in referenced:
        data = getattr(company, i.get_accessor_name()).exists()
        if data:
            is_referenced = True
            break

    if is_referenced:
        return Response({
            "message":"Company data is reference with other model"
        },status.HTTP_401_UNAUTHORIZED)
    company.delete()
    return Response({
        "message":"Data deleted"
    },status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def company_detail(request,pk):
    company = get_object_or_404(Company, pk=pk, context={'request': request})
    serializer = CompanySerializer(company)
    return Response(serializer.data)