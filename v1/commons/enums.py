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


class Style(Enum):
    """
    Uslublar
    """

    artistic = 'badiiy'
    official = 'rasmiy'
    scientific = 'ilmiy'
    publicist = 'publitsistik'
    conversation = "so'zlashuv"
    religious = 'diniy'
    information = 'axborot'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )


class AuthorType(Enum):
    man = 'man'
    woman = 'woman'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )
