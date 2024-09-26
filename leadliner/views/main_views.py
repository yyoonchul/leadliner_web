from flask import Blueprint
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, current_app, request
from leadliner.MakeUserNews import MakeUserNews
from leadliner.GetStockPrice import GetStockPrice
import pandas as pd
import io
from leadliner import db
from datetime import datetime, timedelta

from leadliner.models import UserData, KeywordData, KeywordNewsData

bp = Blueprint('main', __name__, url_prefix='/')

def get_stock_info(stock, get_stock_price):
    data = {
        'name': 'name', 
        'price': 0.00,
        'rate': 0.00
    }

    if stock.korea_stock:
        data['name'] = stock.ko_name
        naver_url = f"https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={stock.ko_name}"
        data['naver_news_link'] = naver_url
        price, rate = get_stock_price.korea_stock_price(stock.stock_code)
        data['price'] = f"{price}원"
        data['rate'] = format(float(rate), ".2f")
    else:
        if stock.ko_name:
            data['name'] = stock.ko_name
            data['naver_news_link'] = f"https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={stock.ko_name}"
        else:
            data['name'] = stock.en_name
        
        data['reuters_news_link'] = f"https://www.reuters.com/site-search/?query={stock.en_name}"
        data['cnbc_news_link'] = f"https://www.cnbc.com/search/?query={stock.en_name}"
        data['yahoo_news_link'] = f"https://finance.yahoo.com/quote/{stock.stock_code}/news/"
        price, rate = get_stock_price.usa_stock_price(stock.stock_code)
        data['price'] = f"{format(float(price or 0), '.2f')}달러"
        data['rate'] = format(float(rate or 0), ".2f")

    return data

def get_news_data(keyword):
    # 현재 시간
    current_time = datetime.now()
    
    # KeywordNewsData에서 해당 키워드의 데이터 조회
    news_data = KeywordNewsData.query.filter_by(keyword=keyword).first()
    
    if news_data is None:
        # 데이터가 없는 경우, 새로운 데이터 생성
        make_user_news = MakeUserNews()
        news = make_user_news.make_user_news(keyword)
        new_data = KeywordNewsData(
            keyword=keyword,
            last_update=current_time,
            news1 = news[0],
            news2 = news[1],
            news3 = news[2]
        )
        db.session.add(new_data)
        db.session.commit()
        return [news[0], news[1], news[2]] 
    
    elif current_time - news_data.last_update > timedelta(hours=1):
        make_user_news = MakeUserNews()
        news = make_user_news.make_user_news(keyword)
        news_data.news1 = news[0]
        news_data.news2 = news[1]
        news_data.news3 = news[2]
        news_data.last_update = current_time
        db.session.commit()
        return [news[0], news[1], news[2]] 
    
    else:
        
        news = [news_data.news1, news_data.news2, news_data.news3]
        return news


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
    
    stock_list = [] #주식 객체
    keyword_list = [] #주식 이름

    for code in code_list:
        stock = KeywordData.query.filter_by(stock_code=code).first()
        stock_list.append(stock)
        if stock.ko_name:
            keyword_list.append(stock.ko_name)
        else:
            keyword_list.append(stock.en_name)

    get_stock_price = GetStockPrice()
    news_data = [get_stock_info(stock, get_stock_price) for stock in stock_list]

    # for data in news_data:
    #     data['news'] = get_news_data(data['name'])

    return render_template('home.html', nickname=user.username, news_data=news_data, keyword_list=keyword_list)

@bp.route('/get_news_data', methods=['POST'])
def get_news_data_route():
    keyword = request.json['keyword']
    news = get_news_data(keyword)
    return jsonify(news)


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