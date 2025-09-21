from django.urls import path
from company.api.views import companylist,createcompany,update_company,company_detail,delete_company

urlpatterns = [
    path('', companylist),
    path('create', createcompany),
    path('update/<int:id>', update_company),
    path('delete/<int:id>', delete_company),
    path('<int:pk>',company_detail, name="company-detail")
]