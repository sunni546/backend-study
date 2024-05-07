from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restx import Namespace, Resource

from models import db, User
from my_jwt import create_token, validate_token, get_user_id

User_api = Namespace(name='User_api', description="API for managing users")

bcrypt = Bcrypt()


@User_api.route('')
class UserGWithJwt(Resource):
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
              "name": "name1",
              "nickname": "nickname1",
              "image": "image1",
              "post_number": 1,
              "follower_number": 0,
              "following_number": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id)

        try:
            user = User.query.filter_by(id=user_id).first()

            result = make_result(user)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@User_api.route('/<int:id>')
@User_api.doc(params={'id': 'User ID'})
class UserG(Resource):
    def get(self, id):
        """
          Get a user item.
        """
        """
          Request:
            GET /users/1
          Returns:
            {
              "id": 1,
              "name": "name1",
              "nickname": "nickname1",
              "image": "image1",
              "post_number": 1,
              "follower_number": 0,
              "following_number": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            user = User.query.filter_by(id=id).first()

            result = make_result(user)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@User_api.route('/<string:nickname>')
@User_api.doc(params={'nickname': 'User nickname'})
class UserGWithNickname(Resource):
    def get(self, nickname):
        """
          Get a user item with nickname.
        """
        """
          Request:
            GET /users/nickname1
          Returns:
            {
              "id": 1,
              "name": "name1",
              "nickname": "nickname1",
              "image": "image1",
              "post_number": 1,
              "follower_number": 0,
              "following_number": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, nickname)

        try:
            user = User.query.filter_by(nickname=nickname).first()

            result = make_result(user)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


def make_result(user):
    result = {
        "id": user.id,
        "name": user.name,
        "nickname": user.nickname,
        "image": user.image,
        "post_number": user.post_number,
        "follower_number": user.follower_number,
        "following_number": user.following_number
    }

    return result


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

        try:
            password_hash = bcrypt.generate_password_hash(password)

            if get_type(phone_email) == 'phone':
                user = User(phone_number=phone_email, name=name, nickname=nickname, password=password_hash)
            elif get_type(phone_email) == 'email':
                user = User(email=phone_email, name=name, nickname=nickname, password=password_hash)
            else:
                return jsonify({'result': "회원가입 실패 - 잘못된 형식의 전화번호 or 이메일입니다."})

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
