from flask import Blueprint
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, current_app, request
from leadliner.MakeUserNews import MakeUserNews
from leadliner.GetStockPrice import GetStockPrice
import pandas as pd
import io

from leadliner.models import UserData, KeywordData

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def home():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.landing'))  # Redirect to signup if no user_id in session
    user = UserData.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('auth.landing'))
    
    #홈화면 뷰 로깅
    current_app.logger.info(f'user{user_id}, main/home, view')

    user_keyword_data = user.keyword_list
    if not user_keyword_data:
       return render_template("home.html", nickname=user.username)
    code_list = user_keyword_data.split(', ')
    
    stock_list = []
    keyword_list = []
    for code in code_list:
        stock = KeywordData.query.filter_by(stock_code=code).first()
        stock_list.append(stock)
        if stock.ko_name:
            keyword_list.append(stock.ko_name)
        else:
            keyword_list.append(stock.en_name)

    make_user_news = MakeUserNews()
    get_stock_price = GetStockPrice()

    news_data = []

    for stock in stock_list:
        data = {
            'name': 'name', 
            'price': 0.00,
            'rate': 0.00}

        if stock.korea_stock:
            data['name'] = stock.ko_name
            naver_url = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query=" + stock.ko_name
            # data['naver_news_link'] = naver_url
            # news = make_user_news.get_naver_news(stock.ko_name, 5) #스트링임
            # news = pd.read_csv(io.StringIO(news))
            # news = news.to_dict(orient="records")
            # data['naver_news'] = news
            price, rate= get_stock_price.korea_stock_price(stock.stock_code)
            data['price'] = price+'원'
            data['rate'] = format(float(rate),".2f")
        else:
            if stock.ko_name:
                data['name'] = stock.ko_name
                base_url = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query="
                url = base_url + stock.ko_name
                data['naver_news_link'] = url
                # news = make_user_news.get_naver_news(stock.ko_name, 5) #스트링임
                # news = pd.read_csv(io.StringIO(news))
                # news = news.to_dict(orient="records")
                # data['naver_news'] = news

            else:
                data['name'] = stock.en_name
            
            reuters_url = "https://www.reuters.com/site-search/?query=" + stock.en_name
            data['reuters_news_link'] = reuters_url
            cnbc_url = "https://www.cnbc.com/search/?query=" + stock.en_name
            data['cnbc_news_link'] = cnbc_url
            yahoo_url = f"https://finance.yahoo.com/quote/{stock.stock_code}/news/"
            data['yahoo_news_link'] = yahoo_url
            price, rate= get_stock_price.usa_stock_price(stock.stock_code)
            if price == '':
                price = 0.00
            if rate == '':
                rate = 0.00
            data['price'] = str(format(float(price),".2f"))+'달러'
            data['rate'] = format(float(rate),".2f")
    
        news_data.append(data)

    return render_template('home.html', nickname=user.username, news_data=news_data, keyword_list=keyword_list)

@bp.route('/log_click', methods=['POST'])
def log_click():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # 로그 기록
    current_app.logger.info(f'user{user_id}, main/home, link_click')

    return jsonify({"status": "success"}), 200

@bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.clear()
    #로그아웃 로깅
    current_app.logger.info(f'user{user_id}, main/logout, logout')
    return redirect(url_for('main.home'))