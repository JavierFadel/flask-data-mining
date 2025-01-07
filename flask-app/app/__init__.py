from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

    # Register Blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    return app