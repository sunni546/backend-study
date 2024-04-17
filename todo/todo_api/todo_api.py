from flask import jsonify, request
from flask_restx import Namespace, Resource, fields

from models import db, Todo
from my_jwt import validate_token, get_user_id

Todo_api = Namespace('Todo_api')

todo_content = Todo_api.model('Todo_content', {
    'content': fields.String(required=True, example="Buy groceries")
})

todo_status = Todo_api.model('Todo_status', {
    'status': fields.Boolean(required=True, example="true")
})


@Todo_api.route('')
class TodoCR(Resource):
    # get_todos
    def get(self):
        """
          Description:
            Get all todo items
        """
        """
          Returns:
            [
              {
                "id": 1,
                "content": "Buy groceries",
                "status": false,
                "user_id": 1
              },
              {
                "id": 2,
                "content": "Do laundry",
                "status": true,
                "user_id": 1
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return "로그인 실패"

        user_id = get_user_id(token)
        print(user_id)

        result = []

        try:
            todos = Todo.query.filter_by(user_id=user_id).all()
            for row in todos:
                result.append(make_result(row))

        except Exception as e:
            print(e)

        return jsonify(result)

    # create_todo
    @Todo_api.expect(todo_content)
    def post(self):
        """
          Description:
            Create a new todo item
        """
        """
          Request:
            {
              "content": "Buy groceries"
            }
          Returns:
            {
              "id": 1,
              "content": "Buy groceries",
              "status": false,
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return "로그인 실패"

        user_id = get_user_id(token)
        content = request.json.get('content')
        print(user_id, content)

        todo = Todo(content=content, status=False, user_id=user_id)

        try:
            db.session.add(todo)
            db.session.commit()

            result = make_result(todo)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Todo_api.route('/<int:id>')
class TodoUD(Resource):
    # update_todo
    @Todo_api.expect(todo_status)
    def patch(self, id):
        """
          Description:
            Update a todo item
        """
        """
          Request:
            PATCH /todos/1
            {
              "status": true
            }
          Returns:
            {
              "id": 1,
              "content": "Buy groceries",
              "status": true,
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return "로그인 실패"

        user_id = get_user_id(token)
        status = request.json.get('status')
        print(user_id, id, status)

        try:
            todo = db.session.get(Todo, id)

            if todo.user_id != user_id:
                return "수정 권한 없음"

            todo.status = status
            db.session.commit()

            result = make_result(todo)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    # delete_todo
    def delete(self, id):
        """
          Description:
            Delete a todo item
        """
        """
          Request:
            DELETE /todos/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return "로그인 실패"

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            todo = db.session.get(Todo, id)

            if todo.user_id != user_id:
                return "삭제 권한 없음"

            db.session.delete(todo)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            return "삭제 실패"

        return jsonify(result)


def make_result(todo):
    result = {
        "id": todo.id,
        "content": todo.content,
        "status": bool(todo.status),  # not not todo.status 도 가능
        "user_id": todo.user_id
    }

    return result
