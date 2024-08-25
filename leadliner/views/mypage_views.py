from flask import Blueprint
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash, current_app
from functools import wraps

from leadliner import db
from leadliner.forms import AccountInfoForm
from leadliner.models import UserData, KeywordData, TopKeywordData

bp = Blueprint('mypage', __name__, url_prefix='/mypage')


@bp.route('/account', methods=('GET', 'POST'))
def my_account():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('main.home'))  # Redirect to signup if no user_id in session
    user = UserData.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('main.home'))
    
    #계정 정보 페이지 뷰 로깅
    current_app.logger.info(f'user{user_id}, mypage/account, view')
    form = AccountInfoForm()
    mailing_list = user.mailing_list
    
    if request.method == 'POST' and form.validate_on_submit():
        user_check = UserData.query.filter_by(email=form.email.data).first()
        
        if (not user_check) or (user_check.email == user.email):
            try:
                user.username = form.username.data
                user.email = form.email.data
                if form.mailing_list.data:
                    user.mailing_list = form.mailing_list.data
                else:
                    user.mailing_list = False
                db.session.commit()
                session['user_id'] = user.id
                return redirect(url_for('main.home'))
            except Exception as e:
                db.session.rollback()
                return jsonify(success=False, message=str(e)), 500
        else:
            flash('다른 계정에 가입한 이메일 주소입니다.')

    return render_template('mypage_account.html', nickname=user.username, email=user.email, form=form, mailing_list=mailing_list)

@bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.clear()
    #계정 정보 페이지 로그아웃 로깅
    current_app.logger.info(f'user{user_id}, mypage/account, logout')
    return redirect(url_for('main.home'))

@bp.route('/withdraw', methods=['POST'])
def withdraw():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="User not authenticated"), 401

    user = UserData.query.get(user_id)
    if not user:
        return jsonify(success=False, message="User not found"), 404

    try:
        db.session.delete(user)
        db.session.commit()

        # 세션 클리어
        session.clear()
        current_app.logger.info(f'user{user_id}, mypage/account, withdraw')
        return jsonify(success=True, redirect_url=url_for('auth.signup'))
    
    except Exception as e:
        current_app.logger.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500


#키워드 편집 페이지

@bp.route('/keyword')
def my_keyword():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('main.home'))  # Redirect to signup if no user_id in session
    user = UserData.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('main.home'))
    
    #키워드 편집 페이지 로깅
    current_app.logger.info(f'user{user_id}, mypage/keyword')
    
    user_keyword_data = user.keyword_list
    user_keyword_list = user_keyword_data.split(', ')
    keyword_list = []
    for keyword in user_keyword_list:
        stock = KeywordData.query.filter_by(stock_code=keyword).first()
        if stock.ko_name:
            keyword_list.append(stock.ko_name)
        else:
            keyword_list.append(stock.en_name)


    pre_set_keyword_data = [keyword.ko_name for keyword in TopKeywordData.query.all()]
    pre_set_keyword_data = [x for x in pre_set_keyword_data if x not in keyword_list]

    mailing_list = user.mailing_list

    return render_template('mypage_keyword.html', keywords=keyword_list, preset_keywords=pre_set_keyword_data, mailing_list = mailing_list)

@bp.route('/save-keywords', methods=['POST'])
def submit_keywords():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="User not authenticated"), 401
    data = request.get_json()
    keywords = data.get('keywords', [])
    agreement = data.get('agreement', False)

    user = UserData.query.get(user_id)
    codes = []
    for keyword in keywords:
        stock = KeywordData.query.filter_by(ko_name=keyword).first()
        if stock:
            codes.append(stock.stock_code)
        else:
            stock = KeywordData.query.filter_by(en_name=keyword).first()
            if stock:
                codes.append(stock.stock_code)
            else:
                continue

    user.keyword_list = ', '.join(codes)
    if agreement:
        user.mailing_list = agreement

    try:
        db.session.commit()
        return jsonify(success=True, redirect_url=url_for('main.home'))
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500