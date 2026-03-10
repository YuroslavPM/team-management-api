from rest_framework import serializers
from teams_management.models.team import Team
from teams_management.models.user_profile import UserProfile
from teams_management.serializers.user_serializer import UserProfileReadSerializer

class TeamReadSerializer(serializers.ModelSerializer):
    users = UserProfileReadSerializer(many= True, read_only=True)
    class Meta: 
        model = Team
        fields = ["id", "name", "users", "created_at", "updated_at"]

class TeamWriteSerializer(serializers.ModelSerializer):
    # using this because this expects PK instead of a full Object
    users = serializers.PrimaryKeyRelatedField(
        many= True,
        queryset= UserProfile.objects.all()
    )
    class Meta: 
        model = Team
        fields = ["id", "name", "users", "created_at", "updated_at"]
