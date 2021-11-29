from flask import Flask
from flask import request
import time
import sched
from flask import render_template
import covid_data_handler
import covid_news_handler

app = Flask(__name__)

all_news = ['']
update_dict = []

s = sched.scheduler(time.time, time.sleep)


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


def schedule_add_news(title):
    e1 = s.enter(120, 1, add_news_article)


def schedule_add_update(title):
    e1 = s.enter(1, 1, add_update_token, kwargs={'t': title})


@app.route('/index')
def hello():
    news = add_news_article()
    data = covid_data_handler.process_covid_data()
    local_rate = data[0]
    nation_rate = round(data[1], 1)
    total_death = data[2]
    h_cases = data[3]

    n_location = 'England'
    loc = covid_data_handler.LOCATION

    s.run(blocking=False)
    text_field = request.args.get('two')

    if text_field:
        schedule_add_update(text_field)

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
