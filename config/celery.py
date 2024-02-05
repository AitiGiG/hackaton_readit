import os 
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings'
)

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'spam' : {
        'task':'apps.account.tasks.send_spam_task',
        'schedule':crontab(hour=23)
    }
}