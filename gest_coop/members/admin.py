# members/admin.py

from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'email', 'role')
    readonly_fields = ('created_at', 'updated_at')
