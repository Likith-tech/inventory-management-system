import logging
import os
import sys

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import inspect
from werkzeug.middleware.proxy_fix import ProxyFix
from config import get_config
from app.utils.helpers import money
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
except ImportError:
    def get_remote_address():
        return 'local'

    class Limiter:
        def __init__(self, *args, **kwargs):
            pass

        def init_app(self, app):
            app.logger.warning('flask-limiter is not installed; login rate limiting is disabled.')

        def limit(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

try:
    from flask_migrate import Migrate
except ImportError:  # Keeps the app runnable until requirements are installed.
    Migrate = None

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
mail = Mail()
migrate = Migrate() if Migrate else None
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=[])

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    configure_logging(app)
    validate_startup_config(app)

    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration(), SqlalchemyIntegration()],
            traces_sample_rate=0.2,
            environment=os.getenv('FLASK_ENV', 'development'),
        )
        app.logger.info('Sentry SDK initialised.')

    if app.config.get('PREFERRED_URL_SCHEME') == 'https':
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    if migrate:
        migrate.init_app(app, db)

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.products import bp as products_bp
    from app.routes.categories import bp as categories_bp
    from app.routes.suppliers import bp as suppliers_bp
    from app.routes.customers import bp as customers_bp
    from app.routes.stock import bp as stock_bp
    from app.routes.sales import bp as sales_bp
    from app.routes.reports import bp as reports_bp
    from app.routes.search import bp as search_bp
    from app.routes.activity_logs import bp as activity_logs_bp
    from app.routes.profile import profile_bp
    from app.routes.notification import notification_bp
    from app.routes.health import bp as health_bp
    from app.routes.admin import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(activity_logs_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(admin_bp)
    csrf.exempt(health_bp)
    register_template_helpers(app)
    register_error_handlers(app)
    register_security_headers(app)

    if should_initialize_database(app):
        initialize_development_database(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))


def is_migration_command():
    """Return True while Flask-Migrate/Alembic is preparing or applying migrations."""
    argv = [arg.lower() for arg in sys.argv]
    if any(arg.endswith('alembic') or arg.endswith('alembic.exe') for arg in argv):
        return True
    return 'db' in argv


def should_initialize_database(app):
    if not app.config.get('AUTO_CREATE_DATABASE'):
        return False
    if is_migration_command():
        app.logger.info('Skipping database bootstrap during migration command.')
        return False
    return True


def user_table_has_current_schema(app):
    """Check the real database before using the User ORM mapper during startup."""
    try:
        inspector = inspect(db.engine)
        if not inspector.has_table('users'):
            app.logger.info('Skipping default admin creation because users table does not exist yet.')
            return False

        existing_columns = {column['name'] for column in inspector.get_columns('users')}
        required_columns = {column.name for column in db.Model.metadata.tables['users'].columns}
        missing_columns = required_columns - existing_columns
        if missing_columns:
            app.logger.info(
                'Skipping default admin creation because users table is missing columns: %s',
                ', '.join(sorted(missing_columns)),
            )
            return False
        return True
    except Exception:
        app.logger.exception('Could not inspect users table; skipping default admin creation.')
        return False


def create_default_admin(app):
    """Create one default admin so the project can run immediately."""
    from app.models import User

    if not app.config.get('ADMIN_PASSWORD'):
        app.logger.warning('ADMIN_PASSWORD is not set; skipping automatic admin creation.')
        return

    if not user_table_has_current_schema(app):
        return

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


def initialize_development_database(app):
    """Create local SQLite tables for convenience; production uses migrations."""
    try:
        with app.app_context():
            db.create_all()
            create_default_admin(app)
    except Exception:
        app.logger.exception('Database initialization failed.')
        raise


def validate_startup_config(app):
    """Fail fast for missing production secrets before Gunicorn starts serving."""
    if app.config.get('REQUIRE_PRODUCTION_CONFIG'):
        if app.config.get('SECRET_KEY') == 'dev-secret-key-change-me':
            raise RuntimeError('SECRET_KEY must be set in production.')
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if database_uri.startswith('sqlite:///'):
            raise RuntimeError('DATABASE_URL must be set to a PostgreSQL URL in production.')


def configure_logging(app):
    level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')

    root = logging.getLogger()
    root.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # File handler for production (rotating)
    if not app.config.get('DEBUG'):
        import os
        from logging.handlers import RotatingFileHandler
        logdir = os.path.join(app.root_path, 'logs')
        os.makedirs(logdir, exist_ok=True)
        fh = RotatingFileHandler(os.path.join(logdir, 'app.log'), maxBytes=10 * 1024 * 1024, backupCount=5)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        root.addHandler(fh)


def register_template_helpers(app):
    app.jinja_env.filters['money'] = money

    @app.context_processor
    def inject_theme():
        from flask_login import current_user
        theme = 'system'
        if current_user.is_authenticated:
            theme = current_user.preferred_theme or 'system'
        return {'user_theme': theme}


def register_security_headers(app):
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        if app.config.get('PREFERRED_URL_SCHEME') == 'https':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        # Inline scripts/styles are allowed for the current Jinja templates; nonce CSP can come later.
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )
        return response


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.exception('Unhandled application error: %s', error)
        return render_template('errors/500.html', title='Server Error'), 500

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return render_template('errors/429.html', title='Too Many Requests'), 429
