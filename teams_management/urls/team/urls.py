from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams_management.views.team_view import TeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]