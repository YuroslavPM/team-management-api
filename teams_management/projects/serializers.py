from rest_framework import serializers

from teams_management.projects.models import Project
from teams_management.teams.models import Team
from teams_management.user_profiles.models import UserProfile


class ProjectReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "status", 
            "admins", "members", "teams",
            "created_at", "updated_at"
        ]

class ProjectWriteSerializer(serializers.ModelSerializer):

    admins = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=UserProfile.objects.all(),
    )
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=UserProfile.objects.all(),
    )
    teams = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "status", 
            "admins", "members", "teams", 
            "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]