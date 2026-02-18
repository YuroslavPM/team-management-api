from rest_framework import viewsets
from teams_management.models.team import Team
from teams_management.serializers.team_serializer import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
