from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCelery.settings')

app = Celery('DjangoCelery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
#app.conf.enable_utc=False
app.conf.update(
    broker_url='redis://127.0.0.1:6379/0',  
    result_backend='redis://127.0.0.1:6379/0',  
    task_serializer='json',  
    result_serializer='json',  
    accept_content=['json'],  
    timezone='Asia/Kolkata',  
    enable_utc=False,  
)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule={ 
        'send_mail_at_':{
            'task':'send_mail_app.task.send_mail_func',
            'schedule':crontab(hour=6, minute=24),
            #'args':(2,0)
        } 
    
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
