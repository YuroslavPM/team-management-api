from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication  
from rest_framework.permissions import IsAuthenticated
from teams_management.models.user_profile import UserProfile
from teams_management.serializers.user_serializer import UserProfileReadSerializer, UserProfileWriteSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return UserProfileWriteSerializer
        
        return UserProfileReadSerializer
    
    @action(detail=False, methods=['get'],url_path='me')
    def me(self, request):
        serializer = UserProfileReadSerializer(request.user.profile)
        return Response(serializer.data)