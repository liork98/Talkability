from flask import Flask
from flask_cors import CORS
from . import create_app

talkability_app = create_app()
CORS(talkability_app)

if __name__ == '__main__':
    talkability_app.run(debug=True)


