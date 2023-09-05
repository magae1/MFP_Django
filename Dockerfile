FROM python:slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 소스코드 복사
COPY /movie_footprints .

# requirements/production.txt의 라이브러리 설치
RUN pip install -r requirements/production.txt

RUN django-admin collectstatic

# 외부 노출 포트 설정
EXPOSE 8000

# WSGI 서버 시작
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
