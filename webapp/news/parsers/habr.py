from datetime import datetime, timedelta
from pymystem3 import Mystem
mystem = Mystem()
import locale
import platform

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.news.models import News

from webapp.news.parsers.utils import get_html, save_news

dict_month = {
        'января': 'Январь', 
        'февраля': 'Февраль', 
        'марта': 'Март', 
        'апреля': 'Апрель', 
        'мая': 'Май', 
        'июня': 'Июнь', 
        'июля': 'Июль', 
        'августа': 'Август', 
        'сентября': 'Сентябрь', 
        'октября': 'Октябрь', 
        'ноября': 'Ноябрь', 
        'декабря': 'Декабрь'
        }
    

def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    elif 'августа' in date_str:
        date_str = date_str.replace('августа', 'Август')
    """
        date_str = mystem.lemmatize(date_str)
        date_str[2] = date_str[2].capitalize()
        date_str = ''.join(date_str)
    """
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()
        


def get_news_snippets():
    html = get_html('https://habr.com/ru/search/?target_type=posts&q=python&order_by=date')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='content-list_posts').findAll('li', class_='content-list__item_post')
        result_news = []
        for news in all_news:
            title = news.find('a', class_='post__title_link').text
            url = news.find('a', class_='post__title_link')['href']
            published = news.find('span', class_='post__time').text
            published = parse_habr_date(published)
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='post__text-html').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()

     
        