from flask import Flask
from settings import SECRET_KEY, DEBUG
from models.db import init_db

from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.tools import tools_bp
from services.user_manager import user_bp
from services.payment import payment_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(payment_bp)

    return app


if __name__ == "__main__":
    init_db()
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
