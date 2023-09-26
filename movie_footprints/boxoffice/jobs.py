import requests

from django.conf import settings


def get_boxoffcie_list(target_date):
    res = requests.get(
        f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={settings.BOXOFFICE_KEY}&targetDt={target_date}"
    )
    data = res.json()
    return data['boxOfficeResult']['dailyBoxOfficeList']


def get_tmdb_data(movieNm: str):
    res = requests.get(
        f"https://api.themoviedb.org/3/search/movie?query={movieNm}&language=ko&region=KR&api_key={settings.TMDB_KEY}"
    )
    data = res.json()
    return data['results'][0]
