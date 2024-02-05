from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class AdminAndManagerObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom obtain serializer for adding user role
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.role == 'customer':
            raise serializers.ValidationError("<< Haddingizdan oshmang. >>")
        data['role'] = user.role
        return data
