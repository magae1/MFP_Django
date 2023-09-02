from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Profile, Account
from .serializers import CreateAccountSerializer, ProfileSerializer
from .permissions import IsMeOrReadOnly


class AccountCreateViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer
    permission_classes = (AllowAny,)


@api_view(['GET'])
@permission_classes((AllowAny,))
def confirm_username(request):
    if not request.query_params:
        return Response({"message": "잘못된 요청입니다."}, status=404)

    username = request.query_params.get('username', None)
    if username is None:
        return Response({"message": "잘못된 요청입니다."}, status=404)

    try:
        Account.objects.get(username=username)
    except ObjectDoesNotExist:
        message, check = "사용 가능한 계정명입니다.", True
    else:
        message, check = "이미 사용 중인 계정명입니다.", False
    return Response({"message": message, "check": check}, status=200)


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsMeOrReadOnly,)
