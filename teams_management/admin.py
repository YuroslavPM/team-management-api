from django.contrib import admin
from .models import Team, UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('displayName', 'get_email', 'isAdmin', 'createdAt')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'createdAt', 'updatedAt')
    filter_horizontal = ('users',)
