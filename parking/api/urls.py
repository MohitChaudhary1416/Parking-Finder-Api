from django.urls import path
from parking.api.views import CompanyAreaView,CompanyAreaPostView,CompanyUpdateDeleteView,CompanyAreaMembershipView,CompanyAreaMembershipPostView,CompanyAreaMemebershipActionView,VechileView,VechilePostView,VechileUpdateView,AreaRatePlanPostView
urlpatterns = [
    path('company-area',CompanyAreaView.as_view()),
    path('company-area-post', CompanyAreaPostView.as_view()),
    path('company-area-action/<int:company_id>/data/<int:company_area_id>', CompanyUpdateDeleteView.as_view()),

    path('area-membership', CompanyAreaMembershipView.as_view()),
    path('area-membership-post/<int:company_id>', CompanyAreaMembershipPostView.as_view()),
    path('area-membership-action/<int:company_id>/<int:area_membership_id>', CompanyAreaMemebershipActionView.as_view()),


    path('vechile',VechileView.as_view()),
    path('vechile-post',VechilePostView.as_view()),
    path('vechile-update/<int:vechile_id>',VechileUpdateView.as_view()),
    path('area-plan-rate/<int:company_id>', AreaRatePlanPostView.as_view()),
    # path()





]
