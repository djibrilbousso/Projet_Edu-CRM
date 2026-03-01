from flask import Flask, redirect, url_for


def create_app():
    app = Flask(__name__)
    app.secret_key = 'edu-crm-secret-key-2026'

    from app.auth.route import auth
    app.register_blueprint(auth, url_prefix='/auth')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app