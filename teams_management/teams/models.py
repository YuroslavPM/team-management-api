from django.db import models

from teams_management.user_profiles.models import UserProfile

class Team(models.Model):
    name = models.CharField(max_length=100, unique=False)
    users = models.ManyToManyField(UserProfile, related_name='teams')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name