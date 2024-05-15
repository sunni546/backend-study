from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import Brand, db

Brand_api = Namespace(name='Brand_api', description="API for managing brands")

brand_fields = Brand_api.model('Brand', {
    'name': fields.String(description='Brand name', required=True, example="Nike")
})


@Brand_api.route('')
class BrandCR(Resource):
    def get(self):
        """
          Get all brands.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "name": "Nike"
              },
              {
                "id": 2,
                "name": "Adidas"
              },
              ...
            ]
        """
        result = []

        try:
            brands = Brand.query.all()
            for brand in brands:
                result.append(make_result(brand))

        except Exception as e:
            print(e)

        return jsonify(result)

    @Brand_api.expect(brand_fields)
    def post(self):
        """
          Create a new brand.
        """
        """
          Request:
            {
              "name": "Nike"
            }
          Returns:
            {
              "id": 1,
              "name": "Nike"
            }
        """
        name = request.json.get('name')
        print(name)

        try:
            brand = Brand(name=name)

            db.session.add(brand)
            db.session.commit()

            result = make_result(brand)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Brand_api.route('/<int:id>')
@Brand_api.doc(params={'id': 'Brand ID'})
class BrandRUD(Resource):
    @Brand_api.expect(brand_fields)
    def get(self, id):
        """
          Get a brand with ID.
        """
        """
          Request:
            GET /brands/1
          Returns:
            {
              "id": 1,
              "name": "Nike"
            }
        """
        print(id)

        try:
            brand = db.session.get(Brand, id)

            result = make_result(brand)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    @Brand_api.expect(brand_fields)
    def patch(self, id):
        """
          Update a brand.
        """
        """
          Request:
            PATCH /brands/3
            {
              "name": "Vans"
            }
          Returns:
            {
              "id": 3,
              "name": "Vans"
            }
        """
        name = request.json.get('name')
        print(id, name)

        try:
            brand = db.session.get(Brand, id)

            brand.name = name
            db.session.commit()

            result = make_result(brand)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a brand.
        """
        """
          Request:
            DELETE /brands/3
          Returns:
            {}
        """
        print(id)

        try:
            brand = db.session.get(Brand, id)

            db.session.delete(brand)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(brand):
    result = {
        'id': brand.id,
        'name': brand.name
    }

    return result
