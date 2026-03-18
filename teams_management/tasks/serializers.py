from rest_framework import serializers

from teams_management.projects.models import Project
from teams_management.tasks.models import Task
from teams_management.user_profiles.models import UserProfile


class TaskReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id", "title", "status", "priority",
            "project", "assigned_user", "created_at", "updated_at"
        ]


class TaskWriteSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Project.objects.all(),
    )

    assignedUser = serializers.PrimaryKeyRelatedField(
        many= True,
        queryset= UserProfile.objects.all()
    )

    class Meta:
        model = Task
        fields = [
            "id", "title", "status", "priority",
            "project", "assigned_user", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]