from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import Category, db

Category_api = Namespace(name='Category_api', description="API for managing categories")

category_fields = Category_api.model('Category', {
    'name': fields.String(description='Category name', required=True, example="Shoes")
})


@Category_api.route('')
class CategoryCR(Resource):
    def get(self):
        """
          Get all categories.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "name": "Shoes"
              },
              {
                "id": 2,
                "name": "Bag"
              },
              ...
            ]
        """
        result = []

        try:
            categories = Category.query.all()
            for category in categories:
                result.append(make_result(category))

        except Exception as e:
            print(e)

        return jsonify(result)

    @Category_api.expect(category_fields)
    def post(self):
        """
          Create a new category.
        """
        """
          Request:
            {
              "name": "Shoes"
            }
          Returns:
            {
              "id": 1,
              "name": "Shoes"
            }
        """
        name = request.json.get('name')
        print(name)

        try:
            category = Category(name=name)

            db.session.add(category)
            db.session.commit()

            result = make_result(category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Category_api.route('/<int:id>')
@Category_api.doc(params={'id': 'Category ID'})
class CategoryRUD(Resource):
    @Category_api.expect(category_fields)
    def get(self, id):
        """
          Get a category with ID.
        """
        """
          Request:
            GET /categories/1
          Returns:
            {
              "id": 1,
              "name": "Shoes"
            }
        """
        print(id)

        try:
            category = db.session.get(Category, id)

            result = make_result(category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    @Category_api.expect(category_fields)
    def patch(self, id):
        """
          Update a category.
        """
        """
          Request:
            PATCH /categories/3
            {
              "name": "Top"
            }
          Returns:
            {
              "id": 3,
              "name": "Top"
            }
        """
        name = request.json.get('name')
        print(id, name)

        try:
            category = db.session.get(Category, id)

            category.name = name
            db.session.commit()

            result = make_result(category)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a category.
        """
        """
          Request:
            DELETE /categories/3
          Returns:
            {}
        """
        print(id)

        try:
            category = db.session.get(Category, id)

            db.session.delete(category)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(category):
    result = {
        'id': category.id,
        'name': category.name
    }

    return result
