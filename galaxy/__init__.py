from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, current_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_login.config import EXEMPT_METHODS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


def rest_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED', False):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return jsonify({
                "error": {
                 "message": "Need Authorization"
                }
            }), 401
        return func(*args, **kwargs)
    return decorated_view


def create_app():
    from .routes.user import user
    from .routes.post import post
    from .routes.main import main
    from .routes.api import api
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    db.create_all(app=app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(main)
    app.register_blueprint(api)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('views/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "msg": "server error"
        }), 500

    @app.template_filter()
    def html2text(html):
        # convert html to raw text
        bs = BeautifulSoup(html, 'html.parser')
        return bs.get_text()

    return app



