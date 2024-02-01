from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from v1.commons.enums import UserRole
from v1.users.managers import (
    AdminManager, CustomManager, MManager, CustomerManager
)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices(), default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["role"]

    objects = CustomManager()

    def __str__(self) -> str:
        return self.phone_number


class Manager(User):
    objects = MManager()

    class Meta:
        proxy = True


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True


class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True

