from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import Size, db
from my_jwt import validate_token

Size_api = Namespace(name='Size_api', description="API for managing sizes")

size_type = Size_api.model('Size', {
    'type': fields.String(description='Size type', required=True, example="240")
})


@Size_api.route('')
class SizeCR(Resource):
    def get(self):
        """
          Get all sizes. | Get all sizes with item ID.
        """
        """
          Request:
            {}
            or
            {
              "item_id": 1
            }
          Returns:
            [
              {
                "id": 1,
                "type": "240",
                "item_id": 1
              },
              {
                "id": 2,
                "type": "245",
                "item_id": 1
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        item_id = request.json.get('item_id')
        print(item_id)

        result = []

        try:
            if item_id:
                sizes = Size.query.filter_by(item_id=item_id).all()

            else:
                sizes = Size.query.all()

            for size in sizes:
                result.append(make_result(size))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new size.
        """
        """
          Request:
            {
              "type": "240",
              "item_id": 1
            }
          Returns:
            {
              "id": 1,
              "type": "240",
              "item_id": 1
            }
        """
        type = request.json.get('type')
        item_id = request.json.get('item_id')
        print(type, item_id)

        try:
            size = Size(type=type, item_id=item_id)

            db.session.add(size)
            db.session.commit()

            result = make_result(size)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Size_api.route('/<int:id>')
@Size_api.doc(params={'id': 'Size ID'})
class SizeRUD(Resource):
    def get(self, id):
        """
          Get a size with ID.
        """
        """
          Request:
            GET /sizes/1
          Returns:
            {
              "id": 1,
              "type": "240",
              "item_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        print(id)

        try:
            size = db.session.get(Size, id)

            result = make_result(size)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    @Size_api.expect(size_type)
    def patch(self, id):
        """
          Update a size.
        """
        """
          Request:
            PATCH /sizes/3
            {
              "type": "250"
            }
          Returns:
            {
              "id": 3,
              "type": "250",
              "item_id": 1
            }
        """
        type = request.json.get('type')
        print(id, type)

        try:
            size = db.session.get(Size, id)

            size.type = type
            db.session.commit()

            result = make_result(size)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a size.
        """
        """
          Request:
            DELETE /sizes/16
          Returns:
            {}
        """
        print(id)

        try:
            size = db.session.get(Size, id)

            db.session.delete(size)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(size):
    result = {
        'id': size.id,
        'type': size.type,
        'item_id': size.item_id
    }

    return result
