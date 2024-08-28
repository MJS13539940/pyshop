# 장고가 시작될 때마다 자동으로 Celery가 로드되도록 함
from pyshop.celery import app as celery_app

__all__ = ['celery_app']
