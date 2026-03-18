from django.db import models

from teams_management.user_profiles.models import UserProfile
from teams_management.projects.models import Project

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class TaskStatus(models.TextChoices):
        Todo =  'todo', 'To Do'
        InProgress= 'in-progress', 'In Progress' 

    status = models.CharField(max_length=12, default=TaskStatus.Todo, choices=TaskStatus.choices)

    class PriorityStatus(models.TextChoices):
        Low =  'low', 'Low'
        Medium= 'medium', 'Medium' 
        High = 'high', 'High'

    priority = models.CharField(max_length=12, choices=PriorityStatus.choices)

    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='project_tasks')
    assigned_user = models.ManyToManyField(UserProfile, related_name='assigned_user_tasks')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
