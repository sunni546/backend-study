from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from api.comment_api import Comment_api
from api.follow_api import Follow_api
from api.like_api import Like_api
from api.post_api import Post_api
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
    title="Insta-Clone",
    description="Instagram Clone Project.",
    terms_url="/",
    authorizations=authorizations
)

api.add_namespace(User_api, '/users')
api.add_namespace(Post_api, '/posts')
api.add_namespace(Follow_api, '/follows')
api.add_namespace(Like_api, '/likes')
api.add_namespace(Comment_api, '/comments')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
