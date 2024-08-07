from flask import Blueprint
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash, current_app
from functools import wraps

from leadliner import db
from leadliner.forms import AccountInfoForm
from leadliner.models import User
from leadliner.models import UserKeywordData, PreSetKeywordData

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

#편집 전 비밀번호 재확인 

#계정정보 편집 페이지

@bp.route('/account', methods=('GET', 'POST'))
def my_account():
    user_id = session.get('user_id')
    #current_app.logger.info(f'{user_id}, view, {url_for('mypage.my_account')}')
    if not user_id:
        return redirect(url_for('main.home'))  # Redirect to signup if no user_id in session
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('main.home'))
    
    form = AccountInfoForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        user_check = User.query.filter_by(email=form.email.data).first()
        
        if (not user_check) or (user_check.email == user.email):
            try:
                user.username = form.username.data
                user.email = form.email.data
                db.session.commit()
                session['user_id'] = user.id
                return redirect(url_for('main.home'))
            except Exception as e:
                db.session.rollback()
                return jsonify(success=False, message=str(e)), 500
        else:
            flash('다른 계정에 가입한 이메일 주소입니다.')
    return render_template('mypage_account.html', nickname=user.username, email=user.email, form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@bp.route('/withdraw', methods=['POST'])
def withdraw():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="User not authenticated"), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify(success=False, message="User not found"), 404

    try:
        UserKeywordData.query.filter_by(uid=user_id).delete()
        db.session.delete(user)
        db.session.commit()

        # 세션 클리어
        session.clear()
        return jsonify(success=True, redirect_url=url_for('auth.signup'))
    
    except Exception as e:
        current_app.logger.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500


#키워드 편집 페이지

@bp.route('/keyword')
def my_keyword():
    user_id = session.get('user_id')
    #current_app.logger.info(f'{user_id}, view, {url_for('mypage.my_keyword')}')
    if not user_id:
        return redirect(url_for('main.home'))  # Redirect to signup if no user_id in session
    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('main.home'))
    user_keyword_data = UserKeywordData.query.filter_by(uid=user_id).first()
    keyword_list = user_keyword_data.keyword_list.split(', ')
    pre_set_keyword_data = PreSetKeywordData.query.get(1).keyword_list.split(', ')
    pre_set_keyword_data = [x for x in pre_set_keyword_data if x not in keyword_list]

    return render_template('mypage_keyword.html', keywords=keyword_list, preset_keywords=pre_set_keyword_data)

@bp.route('/save-keywords', methods=['POST'])
def submit_keywords():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="User not authenticated"), 401
    keywords = request.json.get('keywords', [])
    keyword_list=', '.join(keywords)

    user_keyword_data = UserKeywordData.query.filter_by(uid=user_id).first()
    if user_keyword_data:
        user_keyword_data.keyword_list = keyword_list
    else:
        new_user_keyword_data = UserKeywordData(uid=user_id, keyword_list=keyword_list)
        db.session.add(new_user_keyword_data)

    try:
        db.session.commit()
        return jsonify(success=True, redirect_url=url_for('main.home'))
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500