from flask import Blueprint
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, current_app, request
from leadliner.MakeUserNews import MakeUserNews
import pandas as pd
import io

from leadliner.models import User
from leadliner.models import UserKeywordData

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def home():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to signup if no user_id in session
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('auth.signup'))
    
    #홈화면 뷰 로깅
    current_app.logger.info(f'user{user_id}, main/home, view')

    user_keyword_data = UserKeywordData.query.filter_by(uid=user_id).first()
    if not user_keyword_data:
       return render_template("home.html", nickname=user.username)
    keyword_list = user_keyword_data.keyword_list.split(', ')
    make_user_news = MakeUserNews()
    news_list = make_user_news.make_merged_news(keyword_list)

    if "error" in news_list:
        return render_template("home.html", nickname=user.username)

    df = pd.read_csv(io.StringIO(news_list))
    news_data = df.to_dict(orient="records")
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