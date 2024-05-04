from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, Comment, Post
from my_jwt import validate_token, get_user_id

Comment_api = Namespace(name='Comment_api', description="API for managing comments")


@Comment_api.route('')
class CommentC(Resource):
    def post(self):
        """
          Create a new comment item.
        """
        """
          Request:
            {
              "content": "comment_content1",
              "post_id": 1
            }
          Returns:
            {
              "id": 1,
              "content": "comment_content1",
              "created_at": 2024-05-02 14:12:13,
              "like_number": 0,
              "user_id": 1,
              "post_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)

        post_id = request.json.get('post_id')
        content = request.json.get('content')
        print(user_id, post_id, content)

        try:
            comment = Comment(content=content, post_id=post_id, user_id=user_id)
            db.session.add(comment)

            post = db.session.get(Post, post_id)
            post.comment_number += 1

            db.session.commit()

            result = make_result(comment)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Comment_api.route('/<int:id>')
@Comment_api.doc(params={'id': 'Comment ID'})
class CommentRD(Resource):
    def get(self, id):
        """
          Get a comment item.
        """
        """
          Request:
            GET /comments/1
          Returns:
            {
              "id": 1,
              "content": "comment_content1",
              "created_at": 2024-05-02 14:12:13,
              "like_number": 0,
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
            comment = db.session.get(Comment, id)

            result = make_result(comment)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a comment item.
          Update a post item.
        """
        """
          Request:
            DELETE /comments/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            comment = db.session.get(Comment, id)

            if comment.user_id != user_id:
                return jsonify({'result': "댓글 삭제 실패 - 권한 없음"})

            post = db.session.get(Post, comment.post_id)
            post.comment_number -= 1

            db.session.delete(comment)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "댓글 삭제 실패"}

        return jsonify(result)


@Comment_api.route('/post/<int:id>')
@Comment_api.doc(params={'id': 'Post ID'})
class CommentR(Resource):
    def get(self, id):
        """
          Get all comment items with post id.
        """
        """
          Request:
            GET /comments/post/1
          Returns:
            [
              {
                "id": 1,
                "content": "comment_content1",
                "created_at": 2024-05-02 14:12:13,
                "like_number": 0,
                "user_id": 1,
                "post_id": 1
              },
              {
                "id": 2,
                "content": "comment_content2",
                "created_at": 2024-05-02 14:16:44,
                "like_number": 0,
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
        print(user_id, id)

        result = []

        try:
            comments = Comment.query.filter_by(post_id=id).all()

            for comment in comments:
                result.append(make_result(comment))

        except Exception as e:
            print(e)

        return jsonify(result)


def make_result(comment):
    result = {
        "id": comment.id,
        "content": comment.content,
        "created_at": comment.created_at,
        "like_number": comment.like_number,
        "user_id": comment.user_id,
        "post_id": comment.post_id
    }

    return result
