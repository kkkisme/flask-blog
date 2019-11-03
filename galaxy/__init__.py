from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bs4 import BeautifulSoup
from .config import Config
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


def create_app():
    from .routes.user import user
    from .routes.post import post
    from .routes.main import main
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

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('views/404.html'), 404

    @app.template_filter()
    def html2text(html):
        # convert html to raw text
        bs = BeautifulSoup(html, 'html.parser')
        return bs.get_text()

    return app



