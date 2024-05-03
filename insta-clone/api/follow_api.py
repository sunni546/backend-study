from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, User, Follow
from my_jwt import validate_token, get_user_id

Follow_api = Namespace(name='Follow_api', description="API for managing follows")


@Follow_api.route('/<int:id>')
@Follow_api.doc(params={'id': 'Following ID'})
class Following(Resource):
    def post(self, id):
        """
          Create a new follow item.
          Update a user item.
        """
        """
          Request:
            POST /follows/2
          Returns:
            {
              "id": 1,
              "following_id": "2",
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        if user_id == id:
            return jsonify({'result': "팔로우 실패 - 동일한 사용자입니다."})

        try:
            follow = Follow.query.filter_by(user_id=user_id, following_id=id).first()
            if follow:
                result = {'result': "팔로우 실패 - 이미 팔로우 중인 사용자입니다."}

            else:
                follow = Follow(following_id=id, user_id=user_id)
                db.session.add(follow)

                user = db.session.get(User, user_id)
                user.following_number += 1

                following = db.session.get(User, id)
                following.follower_number += 1

                db.session.commit()

                result = {
                    "id": follow.id,
                    "following_id": follow.following_id,
                    "user_id": follow.user_id
                }

        except Exception as e:
            print(e)
            result = {'result': "팔로우 실패"}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a follow item.
          Update a user item.
        """
        """
          Request:
            DELETE /follows/2
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        if user_id == id:
            return jsonify({'result': "언팔로우 실패 - 동일한 사용자입니다."})

        try:
            follow = Follow.query.filter_by(user_id=user_id, following_id=id).first()

            db.session.delete(follow)

            user = db.session.get(User, user_id)
            user.following_number -= 1

            following = db.session.get(User, id)
            following.follower_number -= 1

            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "언팔로우 실패"}

        return jsonify(result)
