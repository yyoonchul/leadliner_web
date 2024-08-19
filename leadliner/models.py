from leadliner import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False)

class UserKeywordData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    user = db.relationship('User', backref=db.backref('user_keywords'))
    keyword_list = db.Column(db.Text(), nullable=False)

class PreSetKeywordData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    keyword_list = db.Column(db.Text(), nullable=False)