from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

class SignUpForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(message="닉네임은 필수 입력 항목입니다.")])
    email = EmailField('이메일', validators=[DataRequired(), Email(message="유효한 이메일 주소를 입력해야 합니다.")])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), 
        EqualTo('password2', message = '비밀번호가 일치하지 않습니다'), 
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?]{8,}$', message='비밀번호는 영문, 숫자가 혼합된 8자리 이상이어야 합니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email(message="유효한 이메일 주소를 입력해야 합니다.")])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class AccountInfoForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(message="닉네임은 필수 입력 항목입니다.")])
    email = EmailField('이메일', validators=[DataRequired(), Email(message="유효한 이메일 주소를 입력해야 합니다.")])