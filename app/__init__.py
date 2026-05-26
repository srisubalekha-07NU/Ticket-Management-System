from flask import Flask, render_template

from app.config import Config
from app.extensions import db, migrate, jwt, login_manager, scheduler
from app.auth.routes import auth_bp
from app.tickets.routes import tickets_bp
from app.worklogs.routes import worklogs_bp
from app.reports.routes import reports_bp
from app.notifications.service import run_month_end_reminders


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(worklogs_bp)
    app.register_blueprint(reports_bp)

    @app.route('/')
    def home():
        return render_template('index.html')

    if not scheduler.running:
        scheduler.add_job(run_month_end_reminders, 'cron', hour=9)
        scheduler.start()

    return app
