from rest_framework import viewsets
from teams_management.models.project import Project
from teams_management.serializers.project_serializer import ProjectReadSerializer, ProjectWriteSerializer

class ProjectViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Project.objects.prefetch_related(
            'adminIds', 
            'memberIds', 
            'teamIds'
        ).all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ProjectWriteSerializer
        return ProjectReadSerializer