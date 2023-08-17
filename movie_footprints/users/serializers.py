from django.conf import settings

from rest_framework import serializers

from .models import Profile


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username']
        read_only_fields = ['username']


class ProfileSerializer(serializers.ModelSerializer):
    account = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    class Meta:
        model = Profile
        fields = ["account", "avatar", "nickname", "introduction"]
