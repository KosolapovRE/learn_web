from flask import Flask, render_template

from python_org_news import get_python_news
from weather import weather_by_city

def create_app():
    app = Flask(__name__)    

    @app.route('/')
    def hello():
        page_title = 'Новости Python'
        weather = weather_by_city('Moscow,Russia')
        news_list = get_python_news()
        return render_template('index.html', page_title=page_title, weather=weather, news_list=news_list)


