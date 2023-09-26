from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class DailyBoxofficeSerializer(serializers.Serializer):
    rnum = serializers.IntegerField(label=_("순번"))
    rank = serializers.IntegerField(label=_("순위"))
    rankInten = serializers.IntegerField(label=_("전일 대비 순위 증감분"))
    rankOldAndNew = serializers.CharField(label=_("신규진입여부"), max_length=3)
    movieCd = serializers.IntegerField(label=_("영화 코드"))
    movieNm = serializers.CharField(label=_("영화명"))
    openDt = serializers.DateField(label=_("개봉일"))
    audiAcc = serializers.IntegerField(label=_("누적 관객 수"))
    audiCnt = serializers.IntegerField(label=_("당일 관객 수"))
    poster_path = serializers.CharField(label=_("포스터"))
    tmdb_id = serializers.IntegerField(label=_("tmdb 식별코드"))


class DailyBoxofficeListSerializer(serializers.Serializer):
    target_date = serializers.DateField()
    list = DailyBoxofficeSerializer(many=True)
