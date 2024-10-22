from django.urls import path
from .views import enquiries, enquiry_detail, enquiries_success
from . import views

urlpatterns = [
    path('enquiries/', enquiries, name='enquiries'),
    path('enquiry-detail/<int:enquiry_id>/', enquiry_detail, name='enquiry-detail'),
    path('enquiries-success/<int:pk>/', enquiries_success, name='enquiries_success'),
    path('enquiry-detail/<int:enquiry_id>/', views.enquiry_detail, name='enquiry-detail'),
]