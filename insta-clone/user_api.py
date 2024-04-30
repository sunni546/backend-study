from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restx import Namespace, Resource

from models import db, User, Follow
from my_jwt import create_token, validate_token, get_user_id

User_api = Namespace(name='User_api', description="API for managing users")

bcrypt = Bcrypt()


@User_api.route('/join')
class Join(Resource):
    def post(self):
        """
        Create a new user item.
        """
        """
          Request:
            {
              "phone_email": "01012345678" or "email1@naver.com",
              "name": "name1",
              "nickname": "nickname1",
              "password": "password1"
            }
          Returns:
            {
              "result": "{result}"
            }
        """
        phone_email = request.json.get('phone_email')
        name = request.json.get('name')
        nickname = request.json.get('nickname')
        password = request.json.get('password')
        print(phone_email, name, nickname, password)

        password_hash = bcrypt.generate_password_hash(password)

        if get_type(phone_email) == 'phone':
            user = User(phone_number=phone_email, name=name, nickname=nickname, password=password_hash)
        elif get_type(phone_email) == 'email':
            user = User(email=phone_email, name=name, nickname=nickname, password=password_hash)
        else:
            result = "회원가입 실패 - 잘못된 형식의 전화번호 or 이메일"
            return jsonify({'result': result})

        try:
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
              "phone_nick_email": "01012345678" or "nickname1" or "email1@naver.com",
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
        phone_nick_email = request.json.get('phone_nick_email')
        password = request.json.get('password')
        print(phone_nick_email, password)

        try:
            if get_type(phone_nick_email) == 'phone':
                user = User.query.filter_by(phone_number=phone_nick_email).with_entities(User.id, User.password).first()
            elif get_type(phone_nick_email) == 'email':
                user = User.query.filter_by(email=phone_nick_email).with_entities(User.id, User.password).first()
            else:
                user = User.query.filter_by(nickname=phone_nick_email).with_entities(User.id, User.password).first()

            if bcrypt.check_password_hash(user.password, password):
                result = "로그인 성공"

                return jsonify({'result': result,
                                'jwt': create_token(user.id)})
            else:
                result = "로그인 실패"

        except Exception as e:
            print(e)
            result = "로그인 실패"

        return jsonify({'result': result})


def get_type(p_e):
    if p_e.isdigit() and len(p_e) == 11:
        return 'phone'
    elif '@' in p_e:
        return 'email'
    else:
        return 'another'


@User_api.route('/following/<int:id>')
@User_api.doc(params={'id': 'Following ID'})
class Following(Resource):
    def post(self, id):
        """
          Create a new follow item.
        """
        """
          Request:
            POST /users/follow/2
          Returns:
            {
              "id": 1,
              "following_id": "2",
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return "로그인 실패"

        user_id = get_user_id(token)
        print(user_id, id)

        follow = Follow(following_id=id, user_id=user_id)

        try:
            db.session.add(follow)
            db.session.commit()

            result = {
                "id": follow.id,
                "following_id": follow.following_id,
                "user_id": follow.user_id
            }

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)
