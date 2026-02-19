from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teams_management.views.user_view import UserProfileViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]