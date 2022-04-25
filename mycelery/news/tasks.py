from mycelery.main import app
from myapps.core.news.script.news_script import get_news_from_website

@app.task(name="get_news")
def get_news():
    news_data = get_news_from_website()
    news_data.main()


