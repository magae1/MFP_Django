from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, mixins, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes, OpenApiResponse

from .models import Profile, Account
from .serializers import CreateAccountSerializer, ProfileSerializer
from .permissions import IsMeOrReadOnly


class AccountCreateViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter("identifier", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
        ],
        description='아디이 중복 확인', methods=["GET"],
        responses={
            200: inline_serializer(
                name="아디이 중복 확인 정상 응답",
                fields={
                    "message": serializers.CharField(),
                    "check": serializers.BooleanField(),
            }),
            404: inline_serializer(
                name="아디이 중복 확인 비정상 응답",
                fields={
                    "message": serializers.CharField(),
                }
            )
        }
    )
    @action(detail=False)
    def confirm_identifier(self, request):
        if not request.query_params:
            return Response({"message": "잘못된 요청입니다."}, status=404)

        identifier = request.query_params.get('identifier', None)
        if identifier is None:
            return Response({"message": "잘못된 요청입니다."}, status=404)

        try:
            self.get_queryset().get(identifier=identifier)
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
