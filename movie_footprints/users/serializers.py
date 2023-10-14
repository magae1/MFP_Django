from django.contrib.auth.password_validation import validate_password as validate_pw
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
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


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'identifier', 'last_password_changed', 'profile', 'show_spoiler']
        read_only_fields = ['identifier', 'last_password_changed']


class ChangePasswordSerializer(RetypePasswordMixin, serializers.ModelSerializer):
    old_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Account
        fields = ['old_password', 'password', 're_password']

    def validate(self, attrs):
        if attrs['old_password'] == attrs['password']:
            raise serializers.ValidationError({"password": "새 비밀번호는 기존 비밀번호와 달라야 합니다."})
        attrs = super().validate(attrs)
        return attrs

    def validate_old_password(self, value):
        account = self.instance
        if not account.check_password(value):
            raise serializers.ValidationError({"old_password": "비밀번호가 일치하지 않습니다."})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.last_password_changed = timezone.now()
        instance.save()
        return instance
