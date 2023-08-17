

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [문서화(Document)](#%EB%AC%B8%EC%84%9C%ED%99%94document)
  - [문서 빌드 명령어](#%EB%AC%B8%EC%84%9C-%EB%B9%8C%EB%93%9C-%EB%AA%85%EB%A0%B9%EC%96%B4)
  - [자동 문서화 명령어](#%EC%9E%90%EB%8F%99-%EB%AC%B8%EC%84%9C%ED%99%94-%EB%AA%85%EB%A0%B9%EC%96%B4)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## 문서화(Document)

[cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/index.html)에서 사용하는 문서화 방법을 일부 수정한 문서화입니다.


### 문서 빌드 명령어

- [sphinx-autobuild](https://pypi.org/project/sphinx-autobuild/) 

`/docs`에서 아래의 명령어를 실행:

    $ make livehtml


### 자동 문서화 명령어

`/movie_footprints`의 모든 앱들에 대한 문서를 `/docs/apidocs`에 자동으로 생성한다.

- [sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html): 자동 문서화
- [sphinx.ext.napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html): 구글 파이썬 문서 스타일

`/docs`에서 아래의 명령어를 실행:

    $ make apidocs

