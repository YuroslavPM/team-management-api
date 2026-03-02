from rest_framework.routers import DefaultRouter
from teams_management.views.project_view import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
project_urlpatterns = router.urls
