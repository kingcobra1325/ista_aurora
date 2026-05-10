from lib.clients.news_api import get_news

r = get_news()
print(r.content)
