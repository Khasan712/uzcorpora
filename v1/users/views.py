from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count
from v1.users.serializers import AdminAndManagerObtainPairSerializer, UserSerializerV1
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import User


class AdminAndManagerLoginApi(TokenObtainPairView):
    serializer_class = AdminAndManagerObtainPairSerializer


class UserApiV1(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.filter(is_superuser=False).order_by('-id')
    serializer_class = UserSerializerV1

    def get_queryset(self):
        return super().get_queryset().annotate(
            total_text=Count('user_text__id')
        )
