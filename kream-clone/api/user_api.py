from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restx import Namespace, Resource

from models import db, User
from my_jwt import create_token, validate_token, get_user_id

User_api = Namespace(name='User_api', description="API for managing users")

bcrypt = Bcrypt()


@User_api.route('')
class UserR(Resource):
    def get(self):
        """
          Get a user item with jwt.
        """
        """
          Request:
            GET /users
          Returns:
            {
              "id": 1,
              "email": "email1@naver.com",
              "nickname": "nickname1",
              "image": "image1"
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id)

        try:
            user = User.query.filter_by(id=user_id).first()

            result = {
                "id": user.id,
                "email": user.email,
                "nickname": user.nickname,
                "image": user.image
            }

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@User_api.route('/join')
class Join(Resource):
    def post(self):
        """
        Create a new user item.
        """
        """
          Request:
            {
              "email": "email1@naver.com",
              "password": "password1",
              "shoe_size": 240
            }
          Returns:
            {
              "result": "{result}"
            }
        """
        email = request.json.get('email')
        password = request.json.get('password')
        shoe_size = request.json.get('shoe_size')
        print(email, password, shoe_size)

        try:
            password_hash = bcrypt.generate_password_hash(password)

            user = User(email=email, password=password_hash)
            if shoe_size:
                user.shoe_size = shoe_size

            db.session.add(user)
            db.session.commit()

            result = "회원가입 성공"

        except Exception as e:
            print(e)
            result = "회원가입 실패"

        return jsonify({'result': result})


@User_api.route('/login')
class Login(Resource):
    def post(self):
        """
          Get a user item.
        """
        """
          Request:
            {
              "email": "email1@naver.com",
              "password": "password1"
            }
          Returns:
            {
              "result": "로그인 실패"
            }
            or
            {
              "jwt": "{jwt}",
              "result": "로그인 성공"
            }
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
                result = "로그인 실패 - 이메일 또는 비밀번호를 확인해주세요."

        except Exception as e:
            print(e)
            result = "로그인 실패"

        return jsonify({'result': result})
