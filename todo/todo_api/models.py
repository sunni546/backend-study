from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(16))

    # 연관관계 설정 : one to many
    todos = db.relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, password={self.password!r})"


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(16))
    status = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="todos")

    def __repr__(self):
        return f"Todo(id={self.id!r}, content={self.content!r}, status={self.status!r})"
