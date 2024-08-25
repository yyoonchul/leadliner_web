from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData #개발환경용



# 개발환경용 sqlite이슈
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# db = SQLAlchemy()
# migrate = Migrate()
# 배포때는 그냥 이거 쓰기

def page_not_found(e):
    return render_template('404.html'), 404
def page_not_able(e):
    return render_template('500.html'), 500

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    csrf = CSRFProtect(app)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
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
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_not_able)

    return app