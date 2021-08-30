"""Initialize Flask app."""
from ddtrace import patch_all
from flask import Flask
from flask_assets import Environment
from config import Config

if Config.FLASK_ENV == "production" and Config.DD_SERVICE:
    patch_all()


def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .assets import compile_static_assets
        from .home import home

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        # Compile static assets
        compile_static_assets(assets)

        return app
