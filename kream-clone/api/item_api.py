from datetime import datetime

from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Item, Brand, Category, db

Item_api = Namespace(name='Item_api', description="API for managing items")


@Item_api.route('')
class ItemCR(Resource):
    def get(self):
        """
          Get all items. | Get all items with brand name. | Get all items with category name.
        """
        """
          Request:
            {}
            or
            {
              "brand": "Nike"
            }
            or
            {
              "category": "Shoes"
            }
          Returns:
            [
              {
                "id": 1,
                "name": "Nike Premier 3 TF Black White",
                "image": null,
                "recent_price": 72000,
                "release_price": 140000,
                "model": "AT6178-010",
                "released_at": "2022-02-13",
                "color": "Black/White",
                "transaction_number": 238,
                "interest_number": 0,
                "brand": "Nike",
                "category": "Shoes"
              },
              {
                "id": 2,
                "name": "Adidas Adifom Superstar Mule Core Black",
                "image": null,
                "recent_price": 90000,
                "release_price": null,
                "model": "IG8277",
                "released_at": null,
                "color": "Black/White",
                "transaction_number": 101,
                "interest_number": 0,
                "brand": "Adidas",
                "category": "Shoes"
              },
              ...
            ]
        """
        brand_name = request.json.get('brand')
        category_name = request.json.get('category')
        print(brand_name, category_name)

        result = []
        brand, category = None, None

        try:
            if brand_name and category_name:
                return jsonify({'result': "조회 실패 - 브랜드나 카테고리를 하나만 선택하세요."})

            elif brand_name:
                brand = Brand.query.filter_by(name=brand_name).first()
                items = Item.query.filter_by(brand_id=brand.id).all()

            elif category_name:
                category = Category.query.filter_by(name=category_name).first()
                items = Item.query.filter_by(category_id=category.id).all()

            else:
                items = Item.query.all()

            for item in items:
                if brand_name:
                    category = db.session.get(Category, item.category_id)

                elif category_name:
                    brand = db.session.get(Brand, item.brand_id)

                else:
                    brand = db.session.get(Brand, item.brand_id)
                    category = db.session.get(Category, item.category_id)

                result.append(make_result(item, brand, category))

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def post(self):
        """
          Create a new item.
        """
        """
          Request:
            {
              "name": "Nike Premier 3 TF Black White",
              "release_price": 140000,
              "model": "AT6178-010",
              "released_at": "2022-02-13",
              "color": "Black/White",
              "brand_id": 1,
              "category_id": 1
            }
          Returns:
            {
              "id": 1,
              "name": "Nike Premier 3 TF Black White",
              "image": null,
              "recent_price": null,
              "release_price": 140000,
              "model": "AT6178-010",
              "released_at": "2022-02-13",
              "color": "Black/White",
              "transaction_number": 0,
              "interest_number": 0,
              "brand": "Nike",
              "category": "Shoes"
            }
        """
        name = request.json.get('name')
        image = request.json.get('image')
        release_price = request.json.get('release_price')
        model = request.json.get('model')
        released_at = request.json.get('released_at')
        color = request.json.get('color')
        brand_id = request.json.get('brand_id')
        category_id = request.json.get('category_id')
        print(name, image, release_price, model, released_at, color, brand_id, category_id)

        try:
            if released_at:
                released_at = datetime.strptime(released_at, '%Y-%m-%d')

            item = Item(name=name, image=image, release_price=release_price, model=model, released_at=released_at,
                        color=color, brand_id=brand_id, category_id=category_id)

            db.session.add(item)
            db.session.commit()

            brand = db.session.get(Brand, brand_id)
            category = db.session.get(Category, category_id)

            result = make_result(item, brand, category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Item_api.route('/<int:id>')
@Item_api.doc(params={'id': 'Item ID'})
class ItemRUD(Resource):
    def get(self, id):
        """
          Get an item with ID.
        """
        """
          Request:
            GET /items/1
          Returns:
            {
              "id": 1,
              "name": "Nike Premier 3 TF Black White",
              "image": null,
              "recent_price": null,
              "release_price": 140000,
              "model": "AT6178-010",
              "released_at": "2022-02-13",
              "color": "Black/White",
              "transaction_number": 0,
              "interest_number": 0,
              "brand": "Nike",
              "category": "Shoes"
            }
        """
        print(id)

        try:
            item = db.session.get(Item, id)

            brand = db.session.get(Brand, item.brand_id)
            category = db.session.get(Category, item.category_id)

            result = make_result(item, brand, category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update an item.
        """
        """
          Request:
            PATCH /items/1
            {
              "image": "image1",
              "recent_price": 72000,
              "brand_id": 1
            }
          Returns:
            {
              "id": 1,
              "name": "Nike Premier 3 TF Black White",
              "image": "image1",
              "recent_price": 72000,
              "release_price": 140000,
              "model": "AT6178-010",
              "released_at": "2022-02-13",
              "color": "Black/White",
              "transaction_number": 238,
              "interest_number": 0,
              "brand": "Nike",
              "category": "Shoes"
            }
        """
        name = request.json.get('name')
        image = request.json.get('image')
        recent_price = request.json.get('recent_price')
        release_price = request.json.get('release_price')
        model = request.json.get('model')
        released_at = request.json.get('released_at')
        color = request.json.get('color')
        brand_id = request.json.get('brand_id')
        category_id = request.json.get('category_id')
        print(id, name, image, recent_price, release_price, model, released_at, color, brand_id, category_id)

        try:
            item = db.session.get(Item, id)

            if name:
                item.name = name
            if image:
                item.image = image
            if recent_price:
                item.recent_price = recent_price
            if release_price:
                item.release_price = release_price
            if model:
                item.model = model
            if released_at:
                item.released_at = datetime.strptime(released_at, '%Y-%m-%d')
            if color:
                item.color = color
            if brand_id:
                item.brand_id = brand_id
            if category_id:
                item.category_id = category_id

            db.session.commit()

            brand = db.session.get(Brand, item.brand_id)
            category = db.session.get(Category, item.category_id)

            result = make_result(item, brand, category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete an item.
        """
        """
          Request:
            DELETE /items/1
          Returns:
            {}
        """
        print(id)

        try:
            item = db.session.get(Item, id)

            db.session.delete(item)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(item, brand, category):
    released_at = item.released_at
    if released_at:
        released_at = released_at.strftime('%Y-%m-%d')

    result = {
        'id': item.id,
        'name': item.name,
        'image': item.image,
        'recent_price': item.recent_price,
        'release_price': item.release_price,
        'model': item.model,
        'released_at': released_at,
        'color': item.color,
        'transaction_number': item.transaction_number,
        'interest_number': item.interest_number,
        'brand': brand.name,
        'category': category.name
    }

    return result
