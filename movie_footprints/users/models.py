import uuid
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_otp.util import random_number_token
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def random_name():
    return f'유저_{random_number_token(15)}'


class Profile(models.Model):
    account = models.OneToOneField('Account', on_delete=models.SET_NULL, null=True)
    avatar = ProcessedImageField(verbose_name=_("아바타"),
                                 upload_to='avatars/',
                                 processors=[ResizeToFill(200, 200)],
                                 format='JPEG',
                                 blank=True, null=True)
    nickname = models.CharField(verbose_name=_("닉네임"), default=random_name, max_length=30)
    introduction = models.CharField(verbose_name=_("소개"), max_length=300, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _("프로필")

    def __str__(self):
        return f"{self.nickname}"


class AccountManager(BaseUserManager):
    def _create_account(self, identifier, email, password, **extra_fields):
        if not identifier:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)

        account = self.model(identifier=identifier, email=email, **extra_fields)
        account.password = make_password(password)
        account.save(using=self._db)
        return account

    def create_user(self, identifier, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        account = self._create_account(identifier=identifier, email=email, password=password, **extra_fields)
        Profile.objects.create(account=account)
        return account

    def create_superuser(self, identifier, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        account = self._create_account(identifier=identifier, email=email, password=password, **extra_fields)
        Profile.objects.create(account=account)
        return account


class Account(AbstractUser):
    first_name = None
    last_name = None
    username = None
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_("계정의 고유한 식별자입니다. 계정 생성 시 자동으로 할당됩니다."),
        editable=False)
    identifier = models.CharField(
        _("아이디"),
        max_length=40,
        unique=True,
        help_text=_("5~40자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다."),
        validators=[MinLengthValidator(5), RegexValidator(regex=r'[a-z0-9_\-]+')],
        error_messages={
            "unique": _("이미 존재하는 아이디입니다."),
        },
    )
    last_password_changed = models.DateTimeField(_("최근 비밀번호 변경일"), default=timezone.now)

    USERNAME_FIELD = "identifier"

    objects = AccountManager()

    class Meta:
        verbose_name = _("계정")

    def __str__(self):
        return f'{self.identifier}'
