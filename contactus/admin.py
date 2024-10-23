from django.contrib import admin
from .models import Enquiry

# Register your models here.


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('enquiry_number', 'full_name', 'email', 'resolved')
    search_fields = ('enquiry_number', 'email')
    list_filter = ('resolved',)
