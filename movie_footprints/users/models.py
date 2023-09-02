from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_otp.util import random_number_token


def random_name():
    return f'유저_{random_number_token(15)}'


class Profile(models.Model):
    account = models.OneToOneField('Account', on_delete=models.CASCADE)
    avatar = models.ImageField(_("아바타"), upload_to='profile/', blank=True)
    nickname = models.CharField(verbose_name=_("닉네임"), default=random_name, max_length=30)
    introduction = models.CharField(verbose_name=_("소개"), max_length=300, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _("프로필")

    def __str__(self):
        return f"{self.nickname} - {self.introduction}"


class AccountManager(UserManager):
    def create(self, **fields):
        account = self.create_user(**fields)
        Profile.objects.create(account=account)
        return account


class Account(AbstractUser):
    first_name = None
    last_name = None

    last_password_changed = models.DateTimeField(_("최근 비밀번호 변경일"), default=timezone.now)

    objects = AccountManager()

    class Meta:
        verbose_name = _("계정")
