import datetime
import os
import sched
import time

from flask import Flask
from flask import render_template
from flask import request

import covid_data_handler
import covid_news_handler
from update_scheduler import cancel_update, schedule_update, get_updates

"""
This module handles rendering the front end through django
and sorting notifications
"""

app = Flask(__name__)

DATE_FORMAT = "%Y-%m-%dT%H:%M"

s = sched.scheduler(time.time, time.sleep)

notifications = {}
removed_notifications = set()


def remove_notification(title: str = ""):
    for notification_id, notification in notifications.items():
        if notification["title"] == title:
            notifications.pop(notification_id)
            removed_notifications.add(notification_id)
            break


def get_notifications(refresh: bool = True):
    if refresh:
        news_headlines = covid_news_handler.news_api_request()

        for news_headline in news_headlines:
            news_title = news_headline["title"]
            news_description = news_headline["content"]
            news_id = covid_news_handler.calculate_news_id()

            if not news_id or news_id in notifications or news_id in removed_notifications:
                continue

            notifications[news_id] = {"title": news_title, "content": news_description}
    return notifications.values()


@app.route("/")
@app.route('/index')
def render():
    deleted_alarm_title = request.args.get("update_item", default="")
    notification_title = request.args.get("notif", default="")
    new_update_time = request.args.get("update", default="")
    new_update_title = request.args.get("two", default="")

    if notification_title:
        remove_notification(notification_title)
        notifications = get_notifications(refresh=False)
    else:
        notifications = get_notifications(refresh=not deleted_alarm_title)

    if deleted_alarm_title:
        cancel_update(deleted_alarm_title)

    alarms = get_updates()

    if new_update_time and new_update_title:
        current_day = datetime.date.today()
        day_time = str(current_day) + "T" + str(new_update_time)
        schedule_update(
            title=new_update_title,
            at_time=datetime.datetime.strptime(day_time, DATE_FORMAT)
        )

    data = covid_data_handler.process_covid_data()
    local_rate = round(data[0], 1)
    nation_rate = round(data[1], 1)
    total_death = data[2]
    h_cases = data[3]

    return render_template(os.environ['TEMPLATES_PATH'],
                           title='COVID DATA',
                           news_articles=notifications,
                           updates=alarms,
                           nation_location=os.environ['NATION'],
                           location=os.environ['LOCATION'],
                           local_7day_infections=local_rate,
                           national_7day_infections=nation_rate,
                           hospital_cases=h_cases,
                           deaths_total=total_death)


if __name__ == '__main__':
    app.run()
