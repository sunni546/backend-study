import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with sqlite3.connect("todo.db") as connection:
    cursor = connection.cursor()

    # 테이블 초기화(DROP TABLE)
    # cursor.execute("DROP TABLE IF EXISTS todos")

    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, content TEXT, status BOOLEAN)")
    connection.commit()


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
    data_status = False
    if data[2] == 1:
        data_status = True

    result = {
        "id": data[0],
        "content": data[1],
        "status": data_status
    }
    
    return result


if __name__ == '__main__':
    app.run()
