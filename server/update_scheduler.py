import sched
import time
from threading import Thread
import logging

from flask import Markup

"""
This module handles the scheduling of updating events
"""

__scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

__update_info = {}

__schedules = {}


def get_updates():
    return __update_info.values()


def __trigger_update(update_info):
    __update_info.pop(update_info['title'])


def schedule_update(title, at_time):
    if title not in __update_info:
        new_update = __update(
            title=title,
            scheduled_time=at_time)
        __update_info[title] = new_update
        __schedules[title] = __scheduler.enterabs(
            at_time.timestamp(), 1, lambda: __trigger_update(new_update)
        )

    else:
        logging.error("scheduling update with same name and time")

    return __update_info.values()


def __update(title, scheduled_time):
    return {
        "title": title,
        "scheduled_time": scheduled_time,
        "content": Markup(
            f"""Scheduled at: <strong>{scheduled_time}</strong> <br>"""
        )}


def cancel_update(update_title):
    canceled_alarm = __update_info.pop(update_title)

    __scheduler.cancel(__schedules.pop(update_title))

    logging.info(
        "Update called %s scheduled on %s canceled.",
        update_title,
        canceled_alarm["scheduled_time"],
    )


def run_schedules():
    while True:
        __scheduler.run(blocking=False)


Thread(target=run_schedules).start()
