from rest_framework_simplejwt.views import TokenObtainPairView
from v1.users.serializers import AdminAndManagerObtainPairSerializer


class AdminAndManagerLoginApi(TokenObtainPairView):
    serializer_class = AdminAndManagerObtainPairSerializer
