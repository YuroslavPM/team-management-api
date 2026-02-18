from rest_framework import serializers
from teams_management.models.team import Team
from teams_management.models.user_profile import UserProfile

# GetAll Teams
class TeamSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset = UserProfile.objects.all()
          )
    
    class Meta: 
        model = Team
        fields = ["id", "name", "users", "createdAt", "updatedAt"]