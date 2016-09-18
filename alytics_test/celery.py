import os
from celery import Celery
from kombu import Queue
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alytics_test.settings')

app = Celery('alytics_test', broker='amqp://guest@localhost//')

app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE=settings.TIME_ZONE,
    CELERY_RESULT_BACKEND='amqp://guest@localhost//',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_DEFAULT_QUEUE='default',
    CELERY_DEFAULT_EXCHANGE='default',
    CELERY_DEFAULT_EXCHANGE_TYPE='direct',
    CELERY_DEFAULT_ROUTING_KEY='default',
    CELERY_ROUTES={
        'app.views.get_data': {'queue': 'db_reader'},
        'app.views.calculator': {'queue': 'calculator'},
        'app.views.save_data': {'queue': 'db_writer'}
    },

    CELERY_IMPORTS=('app.views',),
    CELERY_QUEUES=(Queue('default'),
                   Queue('db_reader', routing_key='db_reader'),
                   Queue('calculator', routing_key='calculator'),
                   Queue('db_writer', routing_key='db_writer'))
)
