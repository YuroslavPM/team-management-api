from django.contrib import admin
from .models import Team, UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'get_email', 'is_admin', 'created_at')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    filter_horizontal = ('users',)
