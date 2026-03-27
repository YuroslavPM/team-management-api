from django.db import models
from teams_management.user_profiles.models import UserProfile

class Room(models.Model):
    name = models.CharField(max_length=100, unique= True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_messages(self):
        return self.messages.select_related('user').order_by('-created_at')[:50]

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: {'-created_at'}

    def __str__(self):
        return f'{self.user.display_name}: {self.content[:50]}'