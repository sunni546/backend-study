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

    interests = db.relationship("Interest", back_populates="user")

    def __repr__(self):
        return (f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, "
                f"name={self.name!r}, nickname={self.nickname!r}, phone_number={self.phone_number!r}, "
                f"image={self.image!r}, address={self.address!r}), shoe_size={self.shoe_size!r})")


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    image = db.Column(db.String(255))
    recent_price = db.Column(db.Integer)
    release_price = db.Column(db.Integer)
    model = db.Column(db.String(255))
    released_at = db.Column(db.Date)
    color = db.Column(db.String(32), nullable=False)
    transaction_number = db.Column(db.Integer, nullable=False, default=0)
    interest_number = db.Column(db.Integer, nullable=False, default=0)

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship("Brand", back_populates="items")

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Category", back_populates="items")

    sizes = db.relationship("Size", back_populates="item")

    def __repr__(self):
        return (f"Item(id={self.id!r}, name={self.name!r}, image={self.image!r}, recent_price={self.recent_price!r}, "
                f"release_price={self.release_price!r}, model={self.model!r}, released_at={self.released_at!r}, color={self.color!r}, "
                f"transaction_number={self.transaction_number!r}, interest_number={self.interest_number!r}, "
                f"brand_id={self.brand_id!r}, category_id={self.category_id!r})")


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    items = db.relationship("Item", back_populates="brand")

    def __repr__(self):
        return f"Brand(id={self.id!r}, name={self.name!r})"


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    items = db.relationship("Item", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id!r}, name={self.name!r})"


class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False, default="ONE SIZE")

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Item", back_populates="sizes")

    stocks = db.relationship("Stock", back_populates="size")
    interests = db.relationship("Interest", back_populates="size")

    def __repr__(self):
        return f"Size(id={self.id!r}, type={self.type!r}, item_id={self.item_id!r})"


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    delivery_type = db.Column(db.String(16), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    purchased_at = db.Column(db.Date)

    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    size = db.relationship("Size", back_populates="stocks")

    def __repr__(self):
        return (f"Stock(id={self.id!r}, price={self.price!r}, delivery_type={self.delivery_type!r}, "
                f"status={self.status!r}, purchased_at={self.purchased_at!r}, size_id={self.size_id!r})")


class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)

    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    size = db.relationship("Size", back_populates="interests")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="interests")

    def __repr__(self):
        return f"Interest(id={self.id!r}, size_id={self.size_id!r}, user_id={self.user_id!r})"
