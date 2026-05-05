from django.contrib import admin
from .models import Session, Attendance


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'created_at', 'valid_until', 'token', 'external_token')
    readonly_fields = ('token', 'external_token', 'created_at')
    list_filter = ('date',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'timestamp')
    list_filter = ('session__date',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
