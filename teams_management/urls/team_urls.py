from django.urls import path
from teams_management.views.team_view import TeamViewSet

team_urlpatterns = [
    path('teams/', TeamViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('teams/<int:pk>/', TeamViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    })),
]