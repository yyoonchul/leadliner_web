from flask import Blueprint
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app

from leadliner import db
#from leadliner.forms import SignUpForm
from leadliner.models import UserKeywordData, PreSetKeywordData, User


bp = Blueprint('onboarding', __name__, url_prefix='/onboarding')

@bp.route('/keywords-select')
def keywords_select():
    user_id = session.get('user_id')
    current_app.logger.info(f'user{user_id}, onboarding/keyword-select')
    #current_app.logger.info(f'{user_id}, view, {url_for('onboarding.keywords_select')}')
    if not user_id:
        return redirect(url_for('auth.signup'))  # Redirect to signup if no user_id in session
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.signup')) 
    
    pre_set_keyword_data = PreSetKeywordData.query.get(1).keyword_list.split(', ')
    return render_template('keywords_select.html', keywords=pre_set_keyword_data, user_id=user_id)

@bp.route('/submit-keywords', methods=['POST'])
def submit_keywords():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(success=False, message="User not authenticated"), 401
    keywords = request.json.get('keywords', [])

    user_keyword_data = UserKeywordData(uid=user_id, keyword_list=', '.join(keywords))
    db.session.add(user_keyword_data)
    db.session.commit()
    return jsonify(success=True)

@bp.route('/welcome')
def welcome():
    user_id = session.get('user_id')
    current_app.logger.info(f'user{user_id}, onboarding/welcome')
    #current_app.logger.info(f'{user_id}, view, {url_for('onboarding.welcome')}')
    if not user_id:
        return redirect(url_for('auth.signup'))
    return render_template('welcome.html')
