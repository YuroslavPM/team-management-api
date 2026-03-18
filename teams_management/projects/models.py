from django.db import models

from teams_management.user_profiles.models import UserProfile
from teams_management.teams.models import Team

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'Completed'
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        CANCELLED = 'cancelled', 'Cancelled'

    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)  

    admins = models.ManyToManyField(UserProfile, related_name='admin_project') 
    members = models.ManyToManyField(UserProfile, related_name='member_project')
    teams = models.ManyToManyField(Team, related_name='projects')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name