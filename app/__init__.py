from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.products import bp as products_bp
    from app.routes.categories import bp as categories_bp
    from app.routes.suppliers import bp as suppliers_bp
    from app.routes.stock import bp as stock_bp
    from app.routes.sales import bp as sales_bp
    from app.routes.reports import bp as reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(reports_bp)

    # Automatically create database tables
    with app.app_context():
        from app.models import User
        db.create_all()
        create_default_admin(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_default_admin(app):
    """Create one default admin so the project can run immediately."""
    from app.models import User

    if User.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
        return

    admin = User(
        username=app.config['ADMIN_USERNAME'],
        email=app.config['ADMIN_EMAIL'],
        role='admin',
    )
    admin.set_password(app.config['ADMIN_PASSWORD'])
    db.session.add(admin)
    db.session.commit()
