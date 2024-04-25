from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restx import Namespace, Resource, fields

from models import db, User
from my_jwt import create_token

User_api = Namespace(name='User_api', description="API for managing users")

bcrypt = Bcrypt()

user_fields = User_api.model('User', {
    'email': fields.String(description='User email', required=True, example="email1"),
    'password': fields.String(description='User password', required=True, example="password1")
})


@User_api.route('/join')
class Join(Resource):
    @User_api.expect(user_fields)
    def post(self):
        """
        Create a new user item.
        """
        """
          Request:
            {
              "email": "email1",
              "password": "password1"
            }
          Returns:
            회원가입 성공 | 실패
        """
        email = request.json.get('email')
        password = request.json.get('password')
        print(email, password)

        password_hash = bcrypt.generate_password_hash(password)
        # print(password_hash)

        user = User(email=email, password=password_hash)

        try:
            db.session.add(user)
            db.session.commit()

            result = "회원가입 성공"

        except Exception as e:
            print(e)
            result = "회원가입 실패"

        return result


@User_api.route('/login')
class Login(Resource):
    @User_api.expect(user_fields)
    def post(self):
        """
          Get a user item.
        """
        """
          Request:
            {
              "email": "email1",
              "password": "password1"
            }
          Returns:
            로그인 성공 | 실패
        """
        email = request.json.get('email')
        password = request.json.get('password')
        print(email, password)

        try:
            user = User.query.filter_by(email=email).with_entities(User.id, User.password).first()
            if bcrypt.check_password_hash(user.password, password):
                result = "로그인 성공"

                return jsonify({'result': result,
                                'jwt': create_token(user.id)})
            else:
                result = "로그인 실패"

        except Exception as e:
            print(e)
            result = "로그인 실패"

        return result
