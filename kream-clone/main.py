from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from api.brand_api import Brand_api
from api.category_api import Category_api
from api.interest_api import Interest_api
from api.item_api import Item_api
from api.size_api import Size_api
from api.stock_api import Stock_api
from api.user_api import User_api, bcrypt
from config import Config
from models import db

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

bcrypt.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()

authorizations = {'bearer_auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}

api = Api(
    app,
    version='0.1',
    title="Kream-Clone",
    description="Kream Clone Project.",
    terms_url="/",
    authorizations=authorizations
)

api.add_namespace(User_api, '/users')
api.add_namespace(Item_api, '/items')
api.add_namespace(Brand_api, '/brands')
api.add_namespace(Category_api, '/categories')
api.add_namespace(Size_api, '/sizes')
api.add_namespace(Stock_api, '/stocks')
api.add_namespace(Interest_api, '/interests')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
