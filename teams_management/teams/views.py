from rest_framework import viewsets

from teams_management.teams.models import Team
from teams_management.teams.serializers import TeamReadSerializer, TeamWriteSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TeamWriteSerializer
        
        return TeamReadSerializer
