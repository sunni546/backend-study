from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Post, db, User
from my_jwt import validate_token, get_user_id

Post_api = Namespace(name='Post_api', description="API for managing posts")


@Post_api.route('')
class PostC(Resource):
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


@Post_api.route('/<int:id>')
@Post_api.doc(params={'id': 'Post ID'})
class PostUD(Resource):
    def get(self, id):
        """
          Get a post item.
        """
        """
          Request:
            GET /posts/1
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

        print(id)

        try:
            post = db.session.get(Post, id)

            result = make_result(post)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update a post item.
        """
        """
          Request:
            PATCH /posts/1
            Request:
            {
              "content": "content1-1"
            }
          Returns:
            {
              "id": 1,
              "content": "content1-1",
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
        print(user_id, id, content)

        try:
            post = db.session.get(Post, id)

            if post.user_id != user_id:
                return jsonify({'result': "수정 실패 - 권한 없음"})

            post.content = content
            db.session.commit()

            result = make_result(post)

        except Exception as e:
            print(e)
            result = {'result': "수정 실패"}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a post item.
        """
        """
          Request:
            DELETE /posts/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            post = db.session.get(Post, id)

            if post.user_id != user_id:
                return jsonify({'result': "삭제 실패 - 권한 없음"})

            db.session.delete(post)

            user = db.session.get(User, user_id)
            user.post_number -= 1

            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


@Post_api.route('/user/<int:id>')
@Post_api.doc(params={'id': 'User ID'})
class PostR(Resource):
    def get(self, id):
        """
          Get all post items with user id.
        """
        """
          Request:
            GET /posts/user/1
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

        print(id)

        result = []

        try:
            posts = Post.query.filter_by(user_id=id).all()

            for post in posts:
                result.append(make_result(post))

        except Exception as e:
            print(e)

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
