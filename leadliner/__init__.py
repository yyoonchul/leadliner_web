from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rhaudwls2002'  # 안전한 비밀 키로 설정하세요
    csrf = CSRFProtect(app)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models


    from .views import main_views
    from .views import auth_views
    from .views import mypage_views
    from .views import onboarding_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(onboarding_views.bp)


    return app