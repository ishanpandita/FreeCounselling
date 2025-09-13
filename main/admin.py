from django.contrib import admin

from .models import CounsellingEnquiry

class CounsellingEnquiryAdmin(admin.ModelAdmin):
    list_display=("name","email", "counselling_type", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("counselling_type", "created_at")

admin.site.register(CounsellingEnquiry,CounsellingEnquiryAdmin)