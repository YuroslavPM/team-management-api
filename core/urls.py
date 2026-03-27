from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token 
from django.urls import path, include
from teams_management.chat.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api/', include('teams_management.urls')),
    path('api/login', obtain_auth_token, name='api_token_auth')
]
