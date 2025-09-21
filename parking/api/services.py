from rest_framework.permissions import BasePermission
from parking.models import Company,AreaMembership,Role
from rest_framework.response import Response
from django.contrib.auth.models import User

class IscompanyOwner(BasePermission):
    message = "You are not owner of this company"

    def has_permission(self, request,view):
        company_id = view.kwargs.get('company_id')
        company_area = view.kwargs.get('company_area_id')
        if company_id:
            company = Company.objects.filter(id=company_id,owner=request.user)
            if company:
                return True
        return False
    

class APIServices():
    def success_log(self,message,data,status_code):
        Response({
            "Message":message,
            "data":data
        },status_code)
    
    def error_log(self,error,status_code):
        Response({
            "error":error

        },status_code)

class IsparkingMember(BasePermission):
    def has_permission(self, request, view):
        company_id = view.kwargs.get('company_id')
        request.user
        area_membership = AreaMembership.objects.filter(
            area__company__id = company_id,
            user = request.user,
            role = Role.MANAGER    
        ) 

        if area_membership:
            return True
        return False      

class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)