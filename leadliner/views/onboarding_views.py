from flask import Blueprint
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app

from leadliner import db
from leadliner.models import KeywordData, UserData, TopKeywordData


bp = Blueprint('onboarding', __name__, url_prefix='/onboarding')

@bp.route('/keywords-select')
def keywords_select():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.signup'))  # Redirect to signup if no user_id in session
    
    user = UserData.query.get(user_id)
    if not user:
        return redirect(url_for('auth.signup')) 
    
    #온보딩 키워드 선택 뷰 로깅
    current_app.logger.info(f'user{user_id}, onboarding/keyword-select, view')

    top_keywords = [keyword.ko_name for keyword in TopKeywordData.query.all()]
    
    ko_keywords = [keyword.ko_name for keyword in KeywordData.query.filter_by(korea_stock=True).all()]
    en_keywords = [keyword.en_name for keyword in KeywordData.query.filter_by(korea_stock=False).all()]
    all_keywords = ko_keywords + en_keywords


    return render_template('keywords_select.html', top_keywords=top_keywords, all_keywords=all_keywords ,user_id=user_id)

@bp.route('/submit-keywords', methods=['POST'])
def submit_keywords():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="User not authenticated"), 401
    
    data = request.get_json()
    keywords = data.get('keywords', [])
    agreement = data.get('agreement', False)
    
    codes = []

    for keyword in keywords:
        stock = KeywordData.query.filter_by(ko_name=keyword).first()
        if stock:
            codes.append(stock.stock_code)
        else:
            stock = KeywordData.query.filter_by(en_name=keyword).first()
            codes.append(stock.stock_code)

    user = UserData.query.get(user_id)
    user.keyword_list = ', '.join(codes)
    user.mailing_list = agreement
    db.session.commit()
    
    #온보딩 키워드 제출 로깅
    current_app.logger.info(f'user{user_id}, onboarding/keyword-select, submit')
    return jsonify(success=True)

@bp.route('/welcome')
def welcome():
    user_id = session.get('user_id')


    if not user_id:
        return redirect(url_for('auth.signup'))
    
    #온보딩 웰컴 페이지 뷰 로깅
    current_app.logger.info(f'user{user_id}, onboarding/welcome, view')
    return render_template('welcome.html')
