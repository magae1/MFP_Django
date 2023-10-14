import datetime

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .jobs import get_boxoffcie_list, get_tmdb_data
from .serializers import DailyBoxofficeListSerializer


class BoxOfficeList(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DailyBoxofficeListSerializer

    # @method_decorator(cache_page(60*60*4))
    def get(self, request, format=None):
        update_datetime = timezone.now()
        target_datetime = (update_datetime - datetime.timedelta(days=1))
        target_date = target_datetime.strftime('%Y%m%d')
        data = get_boxoffcie_list(target_date)
        for d in data:
            tmdb_data = get_tmdb_data(d['movieNm'])
            d['poster_path'] = tmdb_data['poster_path']
            d['tmdb_id'] = tmdb_data['id']

        serializer_class = self.get_serializer_class()
        serializer = serializer_class({
            'target_date': target_datetime.date(),
            'updated_at': update_datetime,
            'list': data,
        })
        return Response(serializer.data)
