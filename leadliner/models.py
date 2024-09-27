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
    ko_name = db.Column(db.String(50))
    en_name = db.Column(db.String(100))
    stock_code = db.Column(db.String(10), nullable=False, unique=True)
    korea_stock = db.Column(db.Boolean(), nullable=False, default=False)

class TopKeywordData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ko_name = db.Column(db.String(50))
    en_name = db.Column(db.String(50))
    stock_code = db.Column(db.String(10), nullable=False)
    korea_stock = db.Column(db.Boolean(), nullable=False, default=False)

class KeywordNewsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100))
    last_update = db.Column(db.DateTime())
    news1 = db.Column(db.Text())
    news2 = db.Column(db.Text())
    news3 = db.Column(db.Text())
