from flask import Flask, redirect, url_for


def create_app():
    app = Flask(__name__)
    app.secret_key = 'edu-crm-secret-key-2026'

    from app.auth.route import auth
    from app.dashboard.route import dashboard
    from app.students.route import students_bp
    from app.teachers.route import teachers
    from app.courses.route import courses_bp

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers)
    app.register_blueprint(courses_bp)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    return app