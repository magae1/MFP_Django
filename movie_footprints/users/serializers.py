from django.contrib.auth.password_validation import validate_password as validate_pw
from django.contrib.auth.models import  update_last_login

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from .models import Profile, Account


class RetypePasswordMixin(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    re_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate_password(self, value):
        validate_pw(value)
        return value

    def validate(self, attrs):
        re_password = attrs.pop("re_password")
        if attrs["password"] != re_password:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs


class CreateAccountSerializer(RetypePasswordMixin, serializers.Serializer):
    identifier = serializers.CharField(validators=[UniqueValidator(queryset=Account.objects.all())])
    email = serializers.EmailField(allow_blank=True)

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['account', 'avatar', 'nickname', 'introduction']
        read_only_fields = ['account']


class JWTLogInSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        profile = ProfileSerializer(Profile.objects.get(account=user)).data
        token['nickname'] = profile['nickname']
        token['avatar'] = profile['avatar']
        return token


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'identifier', 'last_password_changed', 'profile']
        read_only_fields = ['identifier', 'last_password_changed']
