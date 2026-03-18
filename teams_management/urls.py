from django.urls import path
from rest_framework.routers import DefaultRouter

from teams_management.tasks.views import TaskViewSet
from teams_management.projects.views import ProjectViewSet
from teams_management.teams.views import TeamViewSet
from teams_management.user_profiles.views import UserProfileViewSet

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="users")
router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = router.urls