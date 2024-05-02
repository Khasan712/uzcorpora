from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from v1.users.views import AdminAndManagerLoginApi, UserApiV1
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('', UserApiV1)


urlpatterns = [
    path('login/admin-manager/', AdminAndManagerLoginApi.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]+router.urls
