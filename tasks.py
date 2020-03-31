# -*- coding: utf-8 -*-
from celery import Celery
from celery.schedules import crontab


from TBTracker_RoutineSpider import run

app = Celery('TBTracker_Tasks', broker='redis://localhost:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # it executes every morning at 3:00 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Work Hard!!!'),
    )

@app.task
def test(arg):
    print(arg)
    run()
