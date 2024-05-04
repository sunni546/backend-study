from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, Post, Like
from my_jwt import validate_token, get_user_id

Like_api = Namespace(name='Like_api', description="API for managing likes")


@Like_api.route('/')
class LikeCR(Resource):
    def get(self):
        """
          Get all like items.
        """
        """
          Request:
            {
              "post_id": 1
            }
            or
            {
              "comment_id": 1
            }
          Returns:
            [
              {
                "id": 1,
                "user_id": 1,
                "post_id": 1
              },
              {
                "id": 2,
                "user_id": 2,
                "post_id": 1
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        post_id = request.json.get('post_id')
        print(user_id, post_id)

        result = []

        try:
            likes = Like.query.filter_by(post_id=post_id).all()

            for like in likes:
                result.append(make_result(like))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new like item.
        """
        """
          Request:
            {
              "post_id": 1
            }
            or
            {
              "comment_id": 1
            }
          Returns:
            {
              "id": 1,
              "user_id": 1,
              "post_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)

        post_id = request.json.get('post_id')
        print(user_id, post_id)

        try:
            like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
            if like:
                result = {'result': "좋아요 실패 - 이미 사용자가 좋아요 한 게시물입니다."}

            else:
                like = Like(post_id=post_id, user_id=user_id)
                db.session.add(like)

                post = db.session.get(Post, post_id)
                post.like_number += 1

                db.session.commit()

                result = make_result(like)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Like_api.route('/<int:id>')
@Like_api.doc(params={'id': 'Like ID'})
class LikeRD(Resource):
    def get(self, id):
        """
          Get a like item.
        """
        """
          Request:
            GET /likes/1
          Returns:
            {
              "id": 1,
              "user_id": 1,
              "post_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            like = db.session.get(Like, id)

            result = make_result(like)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a like item.
          Update a post item.
        """
        """
          Request:
            DELETE /likes/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            like = db.session.get(Like, id)

            if like.user_id != user_id:
                return jsonify({'result': "좋아요 취소 실패 - 권한 없음"})

            post = db.session.get(Post, like.post_id)
            post.like_number -= 1

            db.session.delete(like)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "좋아요 취소 실패"}

        return jsonify(result)


def make_result(like):
    result = {
        "id": like.id,
        "user_id": like.user_id,
        "post_id": like.post_id
    }

    return result