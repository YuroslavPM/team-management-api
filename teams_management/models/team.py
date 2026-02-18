from django.db import models
from .user_profile import UserProfile

class Team(models.Model):
    name = models.CharField(max_length=100, unique=False)
    users = models.ManyToManyField(UserProfile, related_name='teams')

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name