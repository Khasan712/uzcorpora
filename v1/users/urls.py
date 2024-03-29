from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from v1.users.views import AdminAndManagerLoginApi


urlpatterns = [
    path('login/admin-manager/', AdminAndManagerLoginApi.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
