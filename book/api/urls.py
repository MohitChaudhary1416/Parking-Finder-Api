from django.urls import path

from book.api.views import BookParkingView, BookParkingUpdateView,khalti_callback

urlpatterns = [
    path('',BookParkingView.as_view()),
    path('<int:id>',BookParkingUpdateView.as_view()),
    path("callback_url",khalti_callback, name="callback" )

]