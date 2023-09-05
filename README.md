

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [문서화(Documentation)](#%EB%AC%B8%EC%84%9C%ED%99%94documentation)
  - [소스코드 문서화(by. Sphinx)](#%EC%86%8C%EC%8A%A4%EC%BD%94%EB%93%9C-%EB%AC%B8%EC%84%9C%ED%99%94by-sphinx)
    - [문서 빌드 명령어](#%EB%AC%B8%EC%84%9C-%EB%B9%8C%EB%93%9C-%EB%AA%85%EB%A0%B9%EC%96%B4)
    - [자동 문서화 명령어](#%EC%9E%90%EB%8F%99-%EB%AC%B8%EC%84%9C%ED%99%94-%EB%AA%85%EB%A0%B9%EC%96%B4)
  - [API entrypoint 문서화(by. OpenAPI 3.0)](#api-entrypoint-%EB%AC%B8%EC%84%9C%ED%99%94by-openapi-30)
    - [문서화 빌드 명령어](#%EB%AC%B8%EC%84%9C%ED%99%94-%EB%B9%8C%EB%93%9C-%EB%AA%85%EB%A0%B9%EC%96%B4)
    - [문서 보기](#%EB%AC%B8%EC%84%9C-%EB%B3%B4%EA%B8%B0)
      - [도커를 이용한 로컬 서브하기](#%EB%8F%84%EC%BB%A4%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EB%A1%9C%EC%BB%AC-%EC%84%9C%EB%B8%8C%ED%95%98%EA%B8%B0)
      - [스테이징 서버에서 서브하기](#%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%95-%EC%84%9C%EB%B2%84%EC%97%90%EC%84%9C-%EC%84%9C%EB%B8%8C%ED%95%98%EA%B8%B0)
  - [README.md 문서화(by. Doctoc)](#readmemd-%EB%AC%B8%EC%84%9C%ED%99%94by-doctoc)
    - [doctoc 설치](#doctoc-%EC%84%A4%EC%B9%98)
    - [doctoc 실행](#doctoc-%EC%8B%A4%ED%96%89)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# 문서화(Documentation)

## 소스코드 문서화(by. [Sphinx](https://www.sphinx-doc.org/en/master/index.html))
[cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/index.html)에서 사용하는 문서화 방법을 일부 수정한 문서화입니다.

### 문서 빌드 명령어

- [sphinx-autobuild](https://pypi.org/project/sphinx-autobuild/) 

`/docs`에서 아래의 명령어를 실행:

    make livehtml


### 자동 문서화 명령어

`/movie_footprints`의 모든 앱들에 대한 문서를 `/docs/apidocs`에 자동으로 생성한다.

- [sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html): 자동 문서화
- [sphinx.ext.napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html): 구글 파이썬 문서 스타일

`/docs`에서 아래의 명령어를 실행:

    make apidocs

## API entrypoint 문서화(by. [OpenAPI 3.0](https://spec.openapis.org/oas/v3.0.3))

[drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)를 이용한 REST API entrypoint 문서화입니다.

### 문서화 빌드 명령어

`/movie_footprints`에서 아래의 명령어를 실행:
    
    python manage.py spectacular --color --validate  --file schema.yml

### 문서 보기

#### 도커를 이용한 로컬 서브하기

1. `api/schema/`로 접속 시 `schema.yml`파일 다운로드
2. ```docker run -d -p 80:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/schema.yml:/schema.yml swaggerapi/swagger-ui``` 도커 컨테이너로 실행
3. `http://localhost:80`로 접속

#### 스테이징 서버에서 서브하기

1. `config/urls.py`에 아래 path 추가
   
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

2. `api/schema/swagger-ui` 또는, `api/schema/redoc` 접속

## README.md 문서화(by. [Doctoc](https://github.com/thlorenz/doctoc))

[doctoc](https://github.com/thlorenz/doctoc)을 이용해 `README.md` 파일에 인덱스를 자동으로 생성합니다.

### doctoc 설치

    npm install -g doctoc

### doctoc 실행

    doctoc README.md
