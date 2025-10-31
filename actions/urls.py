from django.urls import path
from .views import login_view, post_view, admin_view, ping, get_logs

urlpatterns = [
    path("login/", login_view),
    path("post/", post_view),
    path("admin/", admin_view),
    path("ping/", ping),
    path("logs/", get_logs),
]
