from rest_framework.generics import GenericAPIView
from parking.models import CompanyArea,AreaMembership,Vechile
from rest_framework import status
from parking.api.serializer import CompanyAreaSerializer,CompanyAreaMemebershipSerializer,VechileSerializer,ParkingAreaPlanSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from company.models import Company
from parking.api.services import IscompanyOwner,APIServices,IsparkingMember,IsSuperAdmin
from django.shortcuts import get_object_or_404

class CompanyAreaView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        data = CompanyArea.objects.all()
        serializer = CompanyAreaSerializer(data, many = True)
        return Response({
            "Message":"Company Area Fetch Sucessfully",
            "data":serializer.data
        },status.HTTP_201_CREATED)

class CompanyAreaPostView(GenericAPIView):
    permission_classes = [IsAuthenticated,IscompanyOwner]

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = CompanyAreaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Company Area Created Sucessfully",
                "data":serializer.data
            },status.HTTP_201_CREATED) 
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class CompanyUpdateDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated, IscompanyOwner]

    def put(self,request,company_id,company_area_id):
        data = request.data
        companyarea = get_object_or_404(CompanyArea, pk=company_area_id)
        serializer = CompanyAreaSerializer(data=data, instance = companyarea)

        if serializer.is_valid():
            if companyarea.company.id != request.data['company']:
                return APIServices.error_log(self, "You cannot change the company",status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer.save()
            return Response({
                "Message":"Company Area Updated Sucessfully",
                "data":serializer.data
            },status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def delete(self, request, pk, *args, **kwargs):
        companyarea = get_object_or_404(CompanyArea, pk=pk)
        companyarea.delete()
        return Response({
            "Message": "Company Area Deleted Successfully"
        }, status.HTTP_204_NO_CONTENT)
    



class CompanyAreaMembershipView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        data = AreaMembership.objects.all()
        serializer = CompanyAreaMemebershipSerializer(data, many = True)
        return Response({
            "Message":"Companymembership Fetch Sucessfully",
            "data":serializer.data
        },status.HTTP_201_CREATED)

class CompanyAreaMembershipPostView(GenericAPIView):
    permission_classes = [IsAuthenticated, IscompanyOwner|IsparkingMember]

    def post(self,request,company_id):
        data= request.data
        company = Company.objects.get(id= company_id)
        if company.owner.id == data.get('user'):
            return Response({
                "Message":"Owner Cannot be the member"
            },status.HTTP_401_UNAUTHORIZED)
        serializer = CompanyAreaMemebershipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"CompanyAreaMembership Created Sucessfully",
                "data":serializer.data
            },status.HTTP_201_CREATED) 
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class CompanyAreaMemebershipActionView(GenericAPIView):
    permission_classes = [IsAuthenticated, IscompanyOwner|IsparkingMember]

    def put(self,request,company_id,area_membership_id):
        data = request.data
        company = Company.objects.get(id= company_id)
        if company.owner.id == data.get('user'):
            return Response({
                "Message":"Owner Cannot be the member"
            },status.HTTP_401_UNAUTHORIZED)
        company_area_membership = get_object_or_404(AreaMembership,pk=area_membership_id)
        # company_area_membership = AreaMembership.objects.get(id=area_membership_id)
        serializer = CompanyAreaMemebershipSerializer(data=data, instance = company_area_membership)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message":"CompanyAreaMembership Updated Sucessfully",
                "data":serializer.data
            },status.HTTP_200_OK) 
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)
    


class VechileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        data = Vechile.objects.all()
        serializer = VechileSerializer(data, many = True)
        return Response({
            "Message":"Vechiles Fetch Sucessfully",
            "data":serializer.data
        },status.HTTP_201_CREATED)
    
class VechilePostView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self,request):
        data = request.data
        serializer = VechileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message":"Vechile added Sucessfully",
                "data":serializer.data
            },status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class VechileUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def put(self,request,vechile_id):
        data = request.data
        vechile = get_object_or_404(Vechile,id = vechile_id)
        if not vechile_id:
            return Response({
                "Message":"Id didn't found"
            },status.HTTP_401_UNAUTHORIZED)
        serializer = VechileSerializer(data=data, instance = vechile)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message":"Vechile Updated Sucessfully",
                "data":serializer.data
            },status.HTTP_200_OK)
        
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)

class AreaRatePlanPostView(GenericAPIView):
    permission_classes = [IsAuthenticated, IscompanyOwner|IsparkingMember]

    def post(self, request,company_id,  *args, **kwargs):

        data = request.data
        serialzier = ParkingAreaPlanSerializer(data=data)
        if serialzier.is_valid():
            plan = serialzier.save()
            plan.remaining_space = request.data['no_of_space']
            plan.save()
            return Response({
                "message":"Area plan rate added successfully",
                "data":serialzier.data
            },status.HTTP_201_CREATED)
        return Response(serialzier.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)



    
        








        

    



        

