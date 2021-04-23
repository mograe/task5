import requests
from api_keys import api_key_news_api


def ret_news(cat=None,kw=None):
    if(cat and kw):
        a = requests.get(f"https://newsapi.org/v2/top-headlines?q={kw}&category={cat}&apiKey={api_key_news_api}")
    elif(cat):
        a = requests.get(f"https://newsapi.org/v2/top-headlines?category={cat}&apiKey={api_key_news_api}")
    elif(kw):
        a = requests.get(f"https://newsapi.org/v2/top-headlines?q={kw}&apiKey={api_key_news_api}")
    else:
        a = requests.get(f"https://newsapi.org/v2/top-headlines?apiKey={api_key_news_api}")
    news = []
    for i in a.json()["articles"][:10]:
        news.append(i["title"])
    return news


def ret_news_url(cat=None,kw=None):
    if(cat and kw):
        a = requests.get(f"https://newsapi.org/v2/top-headlines?q={kw}&category={cat}&apiKey={api_key_news_api}")
    elif(cat):
        a = requests.get(f"https://newsapi.org/v2/top-headlines?category={cat}&apiKey={api_key_news_api}")
    elif(kw):
        a = requests.get(f"https://newsapi.org/v2/top-headlines?q={kw}&apiKey={api_key_news_api}")
    else:
        a = requests.get(f"https://newsapi.org/v2/top-headlines?apiKey={api_key_news_api}")
    i=0
    news_url = []
    for i in a.json()["articles"][:10]:
        news_url.append(i["url"])
    return news_url

