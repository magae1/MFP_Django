from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class SocialUsernameValidator(validators.RegexValidator):
    regex = r"^[A-Za-z0-9_]+"
    message = "유저명은 알파벳 소문자, 숫자, 또는 _만 포함될 수 있습니다."
