from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Delivery, db
from my_jwt import validate_token

Delivery_api = Namespace(name='Delivery_api', description="API for managing deliveries")


@Delivery_api.route('')
class DeliveryCR(Resource):
    def get(self):
        """
          Get all deliveries.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "info": "CJ대한통운111111111111",
                "name": "name1",
                "phone_number": "010-1111-1111",
                "address": "address1",
                "request_info": "문 앞에 놓아주세요."
              },
              {
                "id": 2,
                "info": null,
                "name": "name2",
                "phone_number": "010-2222-2222",
                "address": "address2",
                "request_info": null
              },
              ...
            ]
        """
        result = []

        try:
            deliveries = Delivery.query.all()
            for delivery in deliveries:
                result.append(make_result(delivery))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new delivery.
        """
        """
          Request:
            {
              "name": "name1",
              "phone_number": "010-1111-1111",
              "address": "address1"
            }
          Returns:
            {
              "id": 1,
              "info": null,
              "name": "name1",
              "phone_number": "010-1111-1111",
              "address": "address1",
              "request_info": null
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        name = request.json.get('name')
        phone_number = request.json.get('phone_number')
        address = request.json.get('address')
        print(name, phone_number, address)

        try:
            delivery = Delivery(name=name, phone_number=phone_number, address=address)

            db.session.add(delivery)
            db.session.commit()

            result = make_result(delivery)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Delivery_api.route('/<int:id>')
@Delivery_api.doc(params={'id': 'Delivery ID'})
class DeliveryRUD(Resource):
    def get(self, id):
        """
          Get a delivery with ID.
        """
        """
          Request:
            GET /deliveries/1
          Returns:
            {
              "id": 1,
              "info": "CJ대한통운111111111111",
              "name": "name1",
              "phone_number": "010-1111-1111",
              "address": "address1",
              "request_info": "문 앞에 놓아주세요."
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        print(id)

        try:
            delivery = db.session.get(Delivery, id)

            result = make_result(delivery)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update a delivery.
        """
        """
          Request:
            PATCH /deliveries/1
            {
              "info": "CJ대한통운111111111111",
              "name": "name1",
              "phone_number": "010-1111-1111",
              "address": "address1",
              "request_info": "문 앞에 놓아주세요."
            }
          Returns:
            {
              "id": 1,
              "info": "CJ대한통운111111111111",
              "name": "name1",
              "phone_number": "010-1111-1111",
              "address": "address1",
              "request_info": "문 앞에 놓아주세요."
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        info = request.json.get('info')
        name = request.json.get('name')
        phone_number = request.json.get('phone_number')
        address = request.json.get('address')
        request_info = request.json.get('request_info')
        print(id, info, name, phone_number, address, request_info)

        try:
            delivery = db.session.get(Delivery, id)

            if info:
                delivery.info = info
            if name:
                delivery.name = name
            if phone_number:
                delivery.phone_number = phone_number
            if address:
                delivery.address = address
            if request_info:
                delivery.request_info = request_info

            db.session.commit()

            result = make_result(delivery)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a delivery.
        """
        """
          Request:
            DELETE /deliveries/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        print(id)

        try:
            delivery = db.session.get(Delivery, id)

            db.session.delete(delivery)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(delivery):
    result = {
        'id': delivery.id,
        'info': delivery.info,
        'name': delivery.name,
        'phone_number': delivery.phone_number,
        'address': delivery.address,
        'request_info': delivery.request_info
    }

    return result
