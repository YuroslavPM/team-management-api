from django.shortcuts import render
from rest_framework import viewsets
from teams_management.models.user_profile import UserProfile
from teams_management.serializers.user_serializer import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer