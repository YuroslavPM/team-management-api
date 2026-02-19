from django.shortcuts import render
from rest_framework import viewsets
from teams_management.models.user_profile import UserProfile
from teams_management.serializers.user_serializer import UserProfileReadSerializer, UserProfileWriteSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    def get_serializer(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return UserProfileWriteSerializer
        
        return UserProfileReadSerializer