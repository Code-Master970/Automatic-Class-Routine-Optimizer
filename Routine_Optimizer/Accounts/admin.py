from django.contrib import admin

# Register your models here.
# accounts/admin.py
from .models import Faculty 
from Accounts.models import Faculty_Attendence

admin.site.site_header = "Code Master Admin Panel"
admin.site.site_title = "Code Master Admin"
admin.site.index_title = "Welcome to the Admin Dashboard"

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'email','phone_number', 'college_id', 'subject', 'photo')
    search_fields = ('user__username', 'email', 'college_id')

@admin.register(Faculty_Attendence)
class FacultyAttendenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'attendence')
    list_filter = ('attendence',)
    list_editable = ('attendence',)
    search_fields = ('user__username',)
