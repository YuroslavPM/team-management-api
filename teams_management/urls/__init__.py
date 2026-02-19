from .user_urls import user_urlpatterns
from .team_urls import team_urlpatterns

urlpatterns = []
urlpatterns += user_urlpatterns
urlpatterns += team_urlpatterns