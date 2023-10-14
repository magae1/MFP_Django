from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from .models import Profile, Account
from .serializers import (
    CreateAccountSerializer,
    ProfileSerializer,
    AccountSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsMeOrReadOnly, IsMeOnly


class AccountCreateViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsMeOrReadOnly,)
    lookup_field = 'account_id'


class AccountViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    permission_classes = (IsMeOnly, )
    parser_classes = (MultiPartParser, JSONParser)

    def get_serializer_class(self):
        if self.action == 'profile':
            return ProfileSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return AccountSerializer

    def get_object(self):
        if self.request.auth is None:
            raise NotAuthenticated(detail=None, code=None)

        if self.action == 'profile':
            return Profile.objects.get(account=self.request.user)
        return self.request.user

    @action(detail=False, methods=['get', 'post'])
    def profile(self, request, pk=None):
        profile = self.get_object()
        serializer_class = self.get_serializer_class()
        if request.method == 'GET':
            serializer = serializer_class(instance=profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = serializer_class(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['get'])
    def me(self, request, pk=None):
        account_obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=account_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def setting(self, request, pk=None):
        account_obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(account_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'])
    def change_password(self, request, pk=None):
        account_obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(account_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "비밀번호가 성공적으로 변경됐습니다."}, status=status.HTTP_202_ACCEPTED)
