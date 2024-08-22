from leadliner import db

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False)
    keyword_list = db.Column(db.Text())
    mailing_list = db.Column(db.Boolean(), nullable=False, default=False)


class KeywordData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    eng_keyword = db.Column(db.String(50))
    ticker = db.Column(db.String(10))