from flask import Flask
from flask_cors import CORS

def create_app():
    talkability_app = Flask(__name__)
    CORS(talkability_app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow frontend requests
    talkability_app.config['SECRET_KEY'] = 'your_secret_key'

    # Register blueprints
    from .routes import routes
    talkability_app.register_blueprint(routes)

    return talkability_app