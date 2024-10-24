from django.urls import path
from .views import (
    enquiries, enquiry_detail,
    enquiries_success, superuser_enquiries,
    resolve_enquiry
)

urlpatterns = [
    path('enquiries/', enquiries, name='enquiries'),
    path(
        'enquiry-detail/<int:enquiry_id>/',
        enquiry_detail, name='enquiry-detail'
    ),
    path(
        'enquiries-success/<int:pk>/',
        enquiries_success, name='enquiries_success'
    ),
    path(
        'superuser-enquiries/',
        superuser_enquiries, name='superuser_enquiries'
    ),
    path('resolve/<int:enquiry_id>/', resolve_enquiry, name='resolve-enquiry'),
]
