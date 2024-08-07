from flask import Blueprint
from flask import Blueprint, render_template, session, redirect, url_for, jsonify#, current_app
from leadliner.MakeUserNews import MakeUserNews
import pandas as pd
import io

from leadliner.models import User
from leadliner.models import UserKeywordData

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def home():
    user_id = session.get('user_id')
    #current_app.logger.info(f'{user_id}, view, {url_for('main.home')}')
    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to signup if no user_id in session
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('auth.signup'))
    user_keyword_data = UserKeywordData.query.filter_by(uid=user_id).first()
    if not user_keyword_data:
       return render_template("home.html", nickname=user.username)
    keyword_list = user_keyword_data.keyword_list.split(', ')
    make_user_news = MakeUserNews()
    news_list = make_user_news.make_merged_news(keyword_list)

    if "error" in news_list:
        return render_template("home.html", nickname=user.username)
    # CSV 문자열을 Pandas DataFrame으로 변환
    df = pd.read_csv(io.StringIO(news_list))
    
    # 헤더 기준으로 리스트 생성
    news_data = df.to_dict(orient="records")
    return render_template('home.html', nickname=user.username, news_data=news_data)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))