from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet


class CustomManager(BaseUserManager):

    def create_user(self, phone_number, role, password, **extra_fields):
        if not phone_number:
            raise ValueError('User must have phone number')
        if not role:
            raise ValueError("User must have role")
        if not password:
            raise ValueError("User must have password")

        user = self.model(
            phone_number=phone_number,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, role, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, role, password, **extra_fields)


class MManager(CustomManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(role='manager')


class AdminManager(CustomManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(role='admin')


class CustomerManager(CustomManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(role='customer')
