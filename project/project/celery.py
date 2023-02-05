from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
app = Celery("project")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "testings": {
        "task": "scrapper.task.workingTest",
        "schedule": 10,
    }
}


@app.task(bind=True)
def debug_task(self):
    print("hello world")
    print("Request: {0!r}".format(self.request))
