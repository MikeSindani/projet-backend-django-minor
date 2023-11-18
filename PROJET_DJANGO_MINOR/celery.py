import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'PROJET_DJANGO_MINOR.settings')
app = Celery('PROJET_DJANGO_MINOR')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.update(timezone = 'Europe/Athens')
# Retry settings
app.conf.broker_connection_retry_on_startup = True
# Celery Beat Settings
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
       'check-every-second': {
           'task': 'minor_dash.tasks.verify_and_send_data',
           'schedule': 20.0,
},}


'''@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello 10'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(5.0, test.s('hello 5'), name='add every 5')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, add.s(16,16), name='add every calcul')

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=19, minute=10, day_of_week=2),
        test.s('Happy thursday!'),
    )

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)'''