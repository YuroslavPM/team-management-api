from rest_framework import viewsets

from teams_management.projects.models import Project
from teams_management.projects.serializers import ProjectReadSerializer, ProjectWriteSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Project.objects.prefetch_related(
            'admins', 
            'members', 
            'teams'
        ).all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ProjectWriteSerializer
        return ProjectReadSerializer