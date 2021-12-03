from flask import request
import time
import sched
from flask import render_template
from typing import Dict, Any
import os
import covid_news_handler, covid_data_handler

from flask import Flask
import json

app = Flask(__name__)



DATE_FORMAT = "%Y-%m-%dT%H:%M"

all_news = ['']
update_dict = []

s = sched.scheduler(time.time, time.sleep)

__notifications = {}

__removed_notifications = set()


def add_news_article():
    global all_news
    news_dic = covid_news_handler.news_API_request()

    if all_news[0] == '':
        all_news = news_dic
    else:
        all_titles = []
        for i in all_news:
            all_titles.append(i['title'])
        for j in news_dic:
            if j['title'] in all_titles:
                pass
            else:
                all_news.append(j)

    return all_news


def add_update_token(t):
    update_dict.append(
        {'title': t,
         'content': 'C'}
    )


def schedule_add_news():
    s.enter(120, 1, add_news_article)
    print('refresh news')


def schedule_add_update(title):
    s.enter(1, 1, add_update_token, kwargs={'t': title})


def create_notification(title: str, content: str) -> Dict[str, Any]:
    return {"title": title, "content": content}


def remove_notification(title: str = ""):
    for notification_id, notification in __notifications.items():
        # find the notification dict with matching title
        if notification["title"] == title:
            __notifications.pop(notification_id)
            __removed_notifications.add(notification_id)
            break


def get_notifications(refresh=True):
    if refresh:
        news_headlines = covid_news_handler.news_API_request()

        for news_headline in news_headlines:
            news_title = news_headline["title"]
            news_description = news_headline["description"]
            news_id = covid_news_handler.calculate_news_id()

            if (
                not news_id
                or news_id in __notifications
                or news_id in __removed_notifications
            ):
                continue

            __notifications[news_id] = create_notification(title=news_title, content=news_description)
    return __notifications.values()


@app.route("/")
@app.route('/index')
def render():

    # the title of the alarm to be removed
    deleted_alarm_title = request.args.get("alarm_item", default="")
    # the title of the notification to be removed
    notification_title = request.args.get("notif", default="")
    # the time when an alarm will be scheduled
    new_alarm_time = request.args.get("alarm", default="")
    # the title of the alarm
    new_alarm_title = request.args.get("two", default="")
    # whether to include news briefing when the alarm fires
    include_news = request.args.get("news", default="")
    # whether to include weather briefing when the alarm fires
    include_weather = request.args.get("weather", default="")

    """
        if notification_title:
        # the notif param is passed
        # delete the given notification
        remove_notification(notification_title)
        notifications = get_notifications(refresh=False)
    else:
        # refresh the list of notifications when the alarm title is not present
        # because we dont want to fetch news when the user is trying to remove alarms
        notifications = get_notifications(refresh=not deleted_alarm_title)

    if deleted_alarm_title:
        # the alarm_item param is passed
        # delete the given alarm
        cancel_alarm(deleted_alarm_title)

    alarms = get_alarms()

    if new_alarm_time and new_alarm_title:
        # the user wants to schedule an alarm
        schedule_alarm(
            title=new_alarm_title,
            at_time=datetime.datetime.strptime(new_alarm_time, DATE_FORMAT)
        )
    """

    news = add_news_article()
    data = covid_data_handler.process_covid_data()
    local_rate = round(data[0], 1)
    nation_rate = round(data[1], 1)
    total_death = data[2]
    h_cases = data[3]

    n_location = os.environ['NATION']
    loc = os.environ['LOCATION']

    s.run(blocking=False)
    text_field = request.args.get('two')

    news_check = request.args.get('news')

    if text_field:
        schedule_add_update(text_field)
        if news_check:
            schedule_add_news()

    return render_template('index.html',
                           title='COVID DATA',
                           news_articles=news,
                           updates=update_dict,
                           nation_location=n_location,
                           location=loc,
                           local_7day_infections=local_rate,
                           national_7day_infections=nation_rate,
                           hospital_cases=h_cases,
                           deaths_total=total_death)


if __name__ == '__main__':
    app.run()
