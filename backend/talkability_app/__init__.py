from flask import Flask

def create_app():
    talkability_app = Flask(__name__)
    talkability_app.config['SECRET_KEY'] = 'your_secret_key'

    from .routes import routes
    talkability_app.register_blueprint(routes)

    return talkability_app
