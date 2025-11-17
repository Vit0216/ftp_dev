from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'dev'

    db.init_app(app)

    from .routes.upload_routes import upload_bp
    from .routes.update_routes import update_bp
    from .routes.delete_routes import delete_bp
    from .auth.routes import auth_bp
    from .models.user import User


    app.register_blueprint(upload_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para aceder a esta página.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def home():
        return redirect(url_for("upload.index"))

    with app.app_context():
        from .models.user import User
        db.create_all()

    return app
