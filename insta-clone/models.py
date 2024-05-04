from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(8), nullable=False)
    nickname = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    intro = db.Column(db.String(32))
    post_number = db.Column(db.Integer, default=0)
    follower_number = db.Column(db.Integer, default=0)
    following_number = db.Column(db.Integer, default=0)

    follows = db.relationship("Follow", back_populates="user")
    posts = db.relationship("Post", back_populates="user")
    likes = db.relationship("Like", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

    def __repr__(self):
        return (f"User(id={self.id!r}, "
                f"phone_number={self.phone_number!r}, email={self.email!r}, "
                f"name={self.name!r}, nickname={self.nickname!r}, password={self.password!r}, "
                f"image={self.image!r}, intro={self.intro!r}), "
                f"post_number={self.post_number!r}), "
                f"follower_number={self.follower_number!r}, following_number={self.following_number!r})")


class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    following_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="follows")

    def __repr__(self):
        return f"Follow(id={self.id!r}, following_id={self.following_id!r}, user_id={self.user_id!r})"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"))
    like_number = db.Column(db.Integer, default=0)
    comment_number = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="posts")

    likes = db.relationship("Like", back_populates="post")
    comments = db.relationship("Comment", back_populates="post")

    def __repr__(self):
        return (f"User(id={self.id!r}, content={self.content!r}, image={self.image!r}, created_at={self.created_at!r}, "
                f"like_number={self.like_number!r}, comment_number={self.comment_number!r}, user_id={self.user_id!r})")


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="likes")

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship("Post", back_populates="likes")

    def __repr__(self):
        return f"Like(id={self.id!r}, user_id={self.user_id!r}, post_id={self.post_id!r})"


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"))
    like_number = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="comments")

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship("Post", back_populates="comments")

    def __repr__(self):
        return (f"Comment(id={self.id!r}, "
                f"content={self.content!r}, created_at={self.created_at!r}, like_number={self.like_number!r}, "
                f"user_id={self.user_id!r}, post_id={self.post_id!r})")
