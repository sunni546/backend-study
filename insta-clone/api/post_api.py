from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Post, db, User
from my_jwt import validate_token, get_user_id

Post_api = Namespace(name='Post_api', description="API for managing posts")


@Post_api.route('')
class PostCR(Resource):
    def get(self):
        """
          Get all post items.
        """
        """
          Request:
            {}
            or
            {
              "id": 1
            }
          Returns:
            [
              {
                "id": 1,
                "content": "content1",
                "image": "image1",
                "created_at": 2024-05-02 14:12:13,
                "like_number": 0,
                "comment_number": 0
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        id = request.json.get('id')
        print(user_id, id)

        if id:
            user_id = id

        result = []

        try:
            posts = Post.query.filter_by(user_id=user_id).all()

            for post in posts:
                result.append(make_result(post))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new post item.
        """
        """
          Request:
            {
              "content": "content1",
              "image": "image1"
            }
          Returns:
            {
              "id": 1,
              "content": "content1",
              "image": "image1",
              "created_at": 2024-05-02 14:12:13,
              "like_number": 0,
              "comment_number": 0
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)

        content = request.json.get('content')
        image = request.json.get('image')
        print(user_id, content, image)

        try:
            post = Post(content=content, image=image, user_id=user_id)
            db.session.add(post)

            user = db.session.get(User, user_id)
            user.post_number += 1

            db.session.commit()

            result = make_result(post)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


def make_result(post):
    result = {
        "id": post.id,
        "content": post.content,
        "image": post.image,
        "created_at": post.created_at,
        "like_number": post.like_number,
        "comment_number": post.comment_number
    }

    return result