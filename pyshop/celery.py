import os
from celery import Celery

#Celery 커맨드라인 프로그램에 대해 DJANGO_SETTINGS_MODULE 변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyshop.settings') #환경변수, pyshop.settings 할당

#어플리케이션 인스턴스 설정
app = Celery('pyshop')
#오브젝트의 환경정보: namespace 속성은 settings.py 파일에 Celery 관련 설정이 가질 접두사를 지정
#namespace='CELERY'를 설정하면 모든 Celery 설정의 이름에 'CELERY_' 접두사가 포함되어야 함(예: CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
#애플리케이션의 비동기 작업을 자동으로 검색하도록 Celery에 지시
app.autodiscover_tasks()
