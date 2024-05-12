from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from config import Config

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

api = Api(
    app,
    version='0.1',
    title="Kream-Clone",
    description="Kream Clone Project.",
    terms_url="/"
)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
