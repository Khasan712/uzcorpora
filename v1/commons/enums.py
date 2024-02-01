from enum import Enum


class UserRole(Enum):
    admin = 'admin'
    manager = 'manager'
    customer = 'customer'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )
