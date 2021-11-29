import requests
from newsapi import NewsApiClient
from datetime import date
import numpy as np

KEY = '88aa96ff69a44201be768c105e9b11a2'


def news_API_request(covid_terms=None, country='gb'):
    newsapi = NewsApiClient(api_key=KEY)
    responses = []

    if covid_terms is None:
        covid_terms = ['Covid', 'COVID-19', 'coronavirus']

    for term in covid_terms:
        top_headlines = newsapi.get_top_headlines(q=term,
                                                  language='en',
                                                  country=country)
        for article in top_headlines['articles']:
            ti = article['title']
            co = article['content']
            item = {'title': ti, 'content': co}
            responses.append(item)

    count = 1
    for outside in responses:
        t1 = outside['title']
        for interior in responses[count:]:
            if t1 == interior['title']:
                responses.remove(interior)
        count += 1

    return responses


def update_news():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval, 1, news_API_request())
    s.run()

    return news