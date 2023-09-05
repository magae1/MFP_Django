from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile, Account


class RetypePasswordMixin(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    re_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        re_password = attrs.pop("re_password")
        if attrs["password"] != re_password:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs


class CreateAccountSerializer(RetypePasswordMixin, serializers.Serializer):
    identifier = serializers.CharField(validators=[UniqueValidator(queryset=Account.objects.all())])

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
