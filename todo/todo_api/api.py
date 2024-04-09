from datetime import datetime, timedelta

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base, relationship

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secretKey'
app.config['BCRYPT_LEVEL'] = 10
bcrypt = Bcrypt(app)

# 문자열 URL : "dialect+driver://username:password@host:port/database"
engine = create_engine("sqlite:///todo.db", echo=True, future=True)
Base = declarative_base()

SECRET_KEY = app.config['SECRET_KEY']


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

    # 연관관계 설정 : one to many
    todos = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, password={self.password!r})"


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    status = Column(Boolean)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"Todo(id={self.id!r}, content={self.content!r}, status={self.status!r})"


Base.metadata.create_all(engine)


@app.route('/join', methods=['POST'])
def join():
    """
      Description:
        Create a new user item
      Request:
        {
          "email": "email1",
          "password": "password1"
        }
      Returns:
        회원가입 성공 | 실패
    """
    email = request.json['email']
    password = request.json['password']
    print(email, password)

    password_hash = bcrypt.generate_password_hash(password)
    # print(password_hash)

    with Session(engine) as session:
        user = User(email=email, password=password_hash)

        try:
            session.add(user)
            session.commit()

            result = "회원가입 성공"

        except Exception as e:
            print(e)
            result = "회원가입 실패"

        return result


@app.route('/login', methods=['POST'])
def login():
    """
      Description:
        Get a user item
      Request:
        {
          "email": "email1",
          "password": "password1"
        }
      Returns:
        로그인 성공 | 실패
    """
    email = request.json['email']
    password = request.json['password']
    print(email, password)

    with Session(engine) as session:
        try:
            user = session.execute(select(User.id, User.password).where(User.email == email)).first()
            if bcrypt.check_password_hash(user.password, password):
                result = "로그인 성공"

                return jsonify({'result': result,
                                'jwt': create_token(user.id)})
            else:
                result = "로그인 실패"

        except Exception as e:
            print(e)
            result = "로그인 실패"

        return result


def create_token(user_id):
    payload = {
        'email': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=60 * 30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token


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
    with Session(engine) as session:
        result = []

        try:
            todos = session.execute(select(Todo))
            for row in todos:
                result.append(make_result(row.Todo))

        except Exception as e:
            print(e)

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
          "status": false,
          "user_id": 1
        }
    """
    content = request.json['content']
    print(content)

    with Session(engine) as session:
        todo = Todo(content=content, status=False, user_id=1)

        try:
            session.add(todo)
            session.commit()

            result = make_result(todo)

        except Exception as e:
            print(e)
            result = {}

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
          "status": true,
          "user_id": 1
        }
    """
    status = request.json['status']
    print(id, status)

    with Session(engine) as session:
        try:
            todo = session.get(Todo, id)

            todo.status = status
            session.commit()

            result = make_result(todo)

        except Exception as e:
            print(e)
            result = {}

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

    with Session(engine) as session:
        try:
            todo = session.get(Todo, id)

            session.delete(todo)
            session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = make_result(todo)

        return jsonify(result)


def make_result(todo):
    result = {
        "id": todo.id,
        "content": todo.content,
        "status": bool(todo.status),  # not not todo.status 도 가능
        "user_id": todo.user_id
    }

    return result


if __name__ == '__main__':
    app.run()
