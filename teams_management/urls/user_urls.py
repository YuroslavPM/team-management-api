from django.urls import path
from teams_management.views import UserProfileViewSet

user_urlpatterns = [
    path('users/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', UserProfileViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    })),
]