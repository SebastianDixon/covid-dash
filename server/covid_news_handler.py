from newsapi import NewsApiClient
import random
import os

"""
This module handles calling news articles for the front end
"""


def news_API_request(covid_terms=None, country='gb'):
    newsapi = NewsApiClient(api_key=os.environ['KEY'])
    responses = []

    if covid_terms is None:
        covid_terms = ['Covid', 'COVID-19', 'coronavirus']

    for term in covid_terms:
        term = term.lower()
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
    print("news called")
    return responses


def calculate_news_id():
    return random.randint(1, 100000)
