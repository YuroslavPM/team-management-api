from django.db import models
from .user_profile import UserProfile

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(UserProfile, related_name='projects')

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'Completed'
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        CANCELLED = 'cancelled', 'Cancelled'

    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)  

    adminIds = models.ManyToManyField(UserProfile, related_name='admin_project') 
    memberIds = models.ManyToManyField(UserProfile, related_name='member_project')
    teamIds = models.ManyToManyField('Team', related_name='projects')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name