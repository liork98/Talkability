from flask import Flask
from . import create_app
talkability_app = create_app()

if __name__ == '__main__':
    talkability_app.run(debug=True, host='127.0.0.1', port=5000)


