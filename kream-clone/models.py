from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(8))
    nickname = db.Column(db.String(16), unique=True)
    phone_number = db.Column(db.String(16), unique=True)
    image = db.Column(db.String(255))
    address = db.Column(db.String(255))
    shoe_size = db.Column(db.Integer, default=0)

    def __repr__(self):
        return (f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, "
                f"name={self.name!r}, nickname={self.nickname!r}, phone_number={self.phone_number!r}, "
                f"image={self.image!r}, address={self.address!r}), shoe_size={self.shoe_size!r})")
