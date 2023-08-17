from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import SocialUsernameValidator


class Account(AbstractUser):
    first_name = None
    last_name = None

    min_length = 3
    max_length = 50
    username = models.CharField(
        _("username"),
        max_length=max_length,
        unique=True,
        help_text=f"(필수){min_length} ~ {max_length}자 영문 소문자, 숫자, _만 포함될 수 있습니다.",
        validators=[SocialUsernameValidator, MinLengthValidator(min_length)],
        error_messages={
            "unique": _("이미 사용 중인 유저명입니다."),
        },
    )
    last_password_changed = models.DateTimeField(_("최근 비밀번호 변경일"), default=timezone.now)

    objects = UserManager()

    class Meta:
        verbose_name = "계정"
        verbose_name_plural = "계정들"


def avatar_path(instance, filename):
    return f"profile/{instance.user.id}-{filename}"


class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_path, blank=True)
    nickname = models.CharField(max_length=100)
    introduction = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "프로필"

    def __str__(self):
        return f"{self.nickname} - {self.introduction}"
