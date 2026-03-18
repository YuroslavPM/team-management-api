from rest_framework import viewsets

from teams_management.tasks.models import Task
from teams_management.tasks.serializers import TaskReadSerializer, TaskWriteSerializer

class TaskViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Task.objects.prefetch_related(
            'project',
            'assigned_user'
        ).all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TaskWriteSerializer
        return TaskReadSerializer
