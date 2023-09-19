from rest_framework import viewsets, mixins, generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, Account
from .serializers import (
    CreateAccountSerializer,
    ProfileSerializer,
    JWTLogInSerializer,
    AccountSerializer,
)
from .permissions import IsMeOrReadOnly, IsMeOnly


def set_refresh_cookie(response: Response, refresh_token: str) -> Response:
    response.set_cookie(
        key='refresh',
        value=refresh_token,
        path='/api/auth',
        httponly=False,
        max_age=api_settings.REFRESH_TOKEN_LIFETIME,
    )
    response.set_cookie(
        key='isLogIn',
        value=True,
        path='/',
        max_age=api_settings.REFRESH_TOKEN_LIFETIME,
    )
    return response


def delete_refresh_cookie(response: Response) -> Response:
    response.delete_cookie(
        key='refresh',
        path='/api/auth',
    )
    response.delete_cookie(
        key='isLogIn',
        path='/',
    )
    return response


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


class LogInView(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = JWTLogInSerializer

    def post(self, request):
        account_serializer = self.get_serializer(data=request.data)
        try:
            account_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = account_serializer.validated_data
        refresh_token = data['refresh']
        res = Response({"message": "성공적으로 로그인됐습니다."}, status=status.HTTP_200_OK)
        return set_refresh_cookie(res, refresh_token)


class RefreshView(views.APIView):
    authentication_classes = ()

    def post(self, request):
        if 'refresh' not in request.COOKIES:
            return Response(data={"message": "refresh 토큰이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh_token = RefreshToken(request.COOKIES['refresh'])
        except InvalidToken as e:
            return Response(data={"message": "유효하지 않은 refresh 토큰입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        res = Response({"access": str(refresh_token.access_token)}, status=status.HTTP_200_OK)

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh_token.blacklist()
                except AttributeError:
                    pass

            refresh_token.set_jti()
            refresh_token.set_exp()
            refresh_token.set_iat()

            res = set_refresh_cookie(res, str(refresh_token))

        return res


class LogOutView(views.APIView):
    def post(self, request):
        res = Response({"message": "성공적으로 로그아웃됐습니다."}, status=status.HTTP_200_OK)
        return delete_refresh_cookie(res)


class AccountView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        if self.request.auth is None:
            raise NotAuthenticated(detail=None, code=None)
        return self.request.user
