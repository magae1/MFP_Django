from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import Profile, Account
from .serializers import CreateAccountSerializer, ProfileSerializer
from .permissions import IsMeOrReadOnly


class AccountCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsMeOrReadOnly,)
