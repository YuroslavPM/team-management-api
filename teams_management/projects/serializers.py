from rest_framework import serializers

from teams_management.projects.models import Project
from teams_management.teams.models import Team
from teams_management.user_profiles.models import UserProfile


class ProjectReadSerializer(serializers.ModelSerializer):

    admin_display_names = serializers.SerializerMethodField()
    member_display_names = serializers.SerializerMethodField()
    team_names = serializers.SerializerMethodField()

    def get_admin_display_names(self, obj):
        return [u.display_name for u in obj.adminIds.all()]

    def get_member_display_names(self, obj):
        return [u.display_name for u in obj.memberIds.all()]

    def get_team_names(self, obj):
        return [t.name for t in obj.teamIds.all()]

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "status", 
            "admin_display_names", "member_display_names", "team_names",
            "created_at", "updated_at"
        ]

class ProjectWriteSerializer(serializers.ModelSerializer):

    adminIds = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=UserProfile.objects.all(),
        source='admin_project' 
    )
    memberIds = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=UserProfile.objects.all(),
        source='member_project' 
    )
    teamIds = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Team.objects.all(),
        source='teamIds'
    )

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "status", 
            "adminIds", "memberIds", "teamIds", 
            "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]