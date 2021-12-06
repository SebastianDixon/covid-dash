import datetime
import os
import sched
import time

from flask import Flask
from flask import render_template
from flask import request

import covid_data_handler
import covid_news_handler
from alarm_scheduler import cancel_alarm, schedule_alarm, get_alarms

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


def get_notifications(refresh=True):
    if refresh:
        news_headlines = covid_news_handler.news_API_request()

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
    # the title of the alarm to be removed
    deleted_alarm_title = request.args.get("alarm_item", default="")
    # the title of the notification to be removed
    notification_title = request.args.get("notif", default="")

    # the time when an alarm will be scheduled
    new_alarm_time = request.args.get("update", default="")
    # the title of the alarm
    new_alarm_title = request.args.get("two", default="")

    if notification_title:
        remove_notification(notification_title)
        notifications = get_notifications(refresh=False)
    else:
        notifications = get_notifications(refresh=not deleted_alarm_title)

    if deleted_alarm_title:
        # the alarm_item param is passed
        # delete the given alarm
        cancel_alarm(deleted_alarm_title)

    alarms = get_alarms()

    if new_alarm_time and new_alarm_title:
        # the user wants to schedule an alarm
        current_day = datetime.date.today()
        day_time = str(current_day) + "T" + str(new_alarm_time)
        schedule_alarm(
            title=new_alarm_title,
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
