from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


class UserSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'role', 'password', 'first_name', 'last_name', 'created_at', 'updated_at')

        extra_kwargs = {
            'password': {'required': False, 'write_only': True},
            'role': {'required': True},
            'first_name': {'required': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['total_text'] = getattr(instance, 'total_text', 0)
        return res


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
