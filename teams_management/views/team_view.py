from rest_framework import viewsets
from teams_management.models.team import Team
from teams_management.serializers.team_serializer import TeamReadSerializer, TeamWriteSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    def get_serializer(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TeamWriteSerializer
        
        return TeamReadSerializer
