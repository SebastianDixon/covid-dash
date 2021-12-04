import logging
import sched
import time
from flask import Markup
from datetime import datetime
from threading import Thread

__scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

# A map of alarm titles to the corresponding alarm info in the shape of
__alarm_info = {}

# A map of alarm titles to the scheduled event of the alarm
__schedules = {}


def get_alarms():
    return __alarm_info.values()


def schedule_alarm(title, at_time, should_include_news=False):
    time_delay = at_time - datetime.now()

    if time_delay.total_seconds() < 0:
        raise ValueError(f"Invalid alarm time given. Received: {at_time}")

    new_alarm = __alarm(
        title=title,
        scheduled_time=at_time,
        include_news=should_include_news,
    )
    __alarm_info[title] = new_alarm
    __schedules[title] = __scheduler.enterabs(
        at_time.timestamp(), 1, lambda: __trigger_alarm(new_alarm)
    )

    return __alarm_info.values()


def __trigger_alarm(alarm_info):
    __alarm_info.pop(alarm_info["title"])


def cancel_alarm(alarm_title):
    if alarm_title not in __schedules:
        raise ValueError(
            f"The given id: {alarm_title} is not associated with any alarm."
        )

    canceled_alarm = __alarm_info.pop(alarm_title)

    __scheduler.cancel(__schedules.pop(alarm_title))
    logging.info(
        "Alarm titled %s scheduled on %s canceled.",
        alarm_title,
        canceled_alarm["scheduled_time"],
    )


def __run_schedules():
    """
    Keep polling the scheduler queue to see if there are any events queueing.
    """
    while True:
        __scheduler.run()


def __alarm(
        title: str,
        scheduled_time: datetime,
        include_news: bool = False,):

    return {
        "title": title,
        "scheduled_time": scheduled_time,
        "content": Markup(
            f"""Scheduled at: <strong>{scheduled_time}</strong> <br>
            News briefing: <strong>{'enabled' if include_news else 'disabled'}</strong> <br>"""
        ),
        "include_news": include_news}


# start a scheduler polling thread
Thread(target=__run_schedules).start()
