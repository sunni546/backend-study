import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with sqlite3.connect("todo.db") as connection:
    cursor = connection.cursor()

    """
      # 테이블 초기화(DROP TABLE)
      cursor.execute("DROP TABLE IF EXISTS todos")
      cursor.execute("DROP TABLE IF EXISTS users")
    """

    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, content TEXT, status BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id TEXT UNIQUE, password TEXT)")
    connection.commit()


# users 테이블 조회
@app.route('/users', methods=['GET'])
def get_users():
    """
      Description:
        Get all user items
      Returns:
        [
          {
            "id": 1,
            "user_id": "id1",
            "password": "pw1"
          },
          {
            "id": 2,
            "user_id": "id2",
            "password": "pw2"
          },
          ...
        ]
    """
    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        datas = cursor.fetchall()

        result = []
        for data in datas:
            result.append({
                "id": data[0],
                "user_id": data[1],
                "password": data[2]
            })

        return jsonify(result)


@app.route('/join', methods=['POST'])
def join():
    """
      Description:
        Create a new user item
      Request:
        {
          "user_id": "id1",
          "password": "pw1"
        }
      Returns:
        회원가입 성공 | 실패
    """
    user_id = request.json['user_id']
    password = request.json['password']
    print(user_id, password)

    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (user_id, password) VALUES (?, ?)", (user_id, password))
        connection.commit()

        cursor.execute("SELECT * FROM users WHERE id=(SELECT MAX(id) FROM users)")
        data = cursor.fetchone()

        result = "회원가입 실패"
        if data:
            if data[1] == user_id and data[2] == password:
                result = "회원가입 성공"

        return result


@app.route('/login', methods=['POST'])
def login():
    """
      Description:
        Get a user item
      Request:
        {
          "user_id": "id1",
          "password": "pw1"
        }
      Returns:
        로그인 성공 | 실패
    """
    user_id = request.json['user_id']
    password = request.json['password']
    print(user_id, password)

    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
        data = cursor.fetchone()

        result = "로그인 실패"
        if data:
            if data[1] == user_id and data[2] == password:
                result = "로그인 성공"

        return result


@app.route('/todos', methods=['GET'])
def get_todos():
    """
      Description:
        Get all todo items
      Returns:
        [
          {
            "id": 1,
            "content": "Buy groceries",
            "status": false
          },
          {
            "id": 2,
            "content": "Do laundry",
            "status": true
          },
          ...
        ]
    """
    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM todos")
        datas = cursor.fetchall()

        result = []
        for data in datas:
            result.append(make_result(data))

        return jsonify(result)


@app.route('/todos', methods=['POST'])
def create_todo():
    """
      Description:
        Create a new todo item
      Request:
        {
          "content": "Buy groceries"
        }
      Returns:
        {
          "id": 1,
          "content": "Buy groceries",
          "status": false
        }
    """
    content = request.json['content']
    print(content)

    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("INSERT INTO todos (content, status) VALUES (?, False)", (content, ))
        connection.commit()

        cursor.execute("SELECT * FROM todos WHERE id=(SELECT MAX(id) FROM todos)")
        data = cursor.fetchone()

        result = {}
        if data:
            result = make_result(data)

        return jsonify(result)


@app.route('/todos/<int:id>', methods=['PATCH'])
def update_todo(id):
    """
      Description:
        Update a todo item
      Request:
        PATCH /todos/1
        {
          "status": true
        }
      Returns:
        {
          "id": 1,
          "content": "Buy groceries",
          "status": true
        }
    """
    status = request.json['status']
    print(id, status)

    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("UPDATE todos SET status=? WHERE id=?", (status, id))
        connection.commit()

        cursor.execute("SELECT * FROM todos WHERE id=?", (id, ))
        data = cursor.fetchone()

        result = {}
        if data:
            result = make_result(data)

        return jsonify(result)


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """
      Description:
        Delete a todo item
      Request:
        DELETE /todos/1
      Returns:
        {}
    """
    print(id)

    with sqlite3.connect("todo.db") as connection:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM todos WHERE id=?", (id, ))
        connection.commit()

        cursor.execute("SELECT * FROM todos WHERE id=?", (id, ))
        data = cursor.fetchone()

        result = {}
        if data:
            result = make_result(data)

        return jsonify(result)


def make_result(data):
    result = {
        "id": data[0],
        "content": data[1],
        "status": bool(data[2])     # not not data[2]도 가능
    }
    
    return result


if __name__ == '__main__':
    app.run()
