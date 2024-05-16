from datetime import datetime

from flask import request, jsonify
from flask_restx import Namespace, Resource

from config import DELIVERY_TYPE
from models import db, Stock
from my_jwt import validate_token

Stock_api = Namespace(name='Stock_api', description="API for managing stocks")


@Stock_api.route('')
class StockCR(Resource):
    def get(self):
        """
          Get all stocks. | Get all stocks with size ID.
        """
        """
          Request:
            {}
            or
            {
              "size_id": 1
            }
          Returns:
            [
              {
                "id": 1,
                "price": 89000,
                "delivery_type": "빠른 배송",
                "status": false,
                "purchased_at": null,
                "size_id": 1
              },
              {
                "id": 2,
                "price": 90000,
                "delivery_type": "일반 배송",
                "status": false,
                "purchased_at": null,
                "size_id": 1
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        size_id = request.json.get('size_id')
        print(size_id)

        result = []

        try:
            if size_id:
                stocks = Stock.query.filter_by(size_id=size_id).all()

            else:
                stocks = Stock.query.all()

            for stock in stocks:
                result.append(make_result(stock))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new stock.
        """
        """
          Request:
            {
              "price": 89000,
              "delivery_type": 0,
              "size_id": 1
            }
          Returns:
            {
              "id": 1,
              "price": 89000,
              "delivery_type": "빠른 배송",
              "status": false,
              "purchased_at": null,
              "size_id": 1
            }
        """
        price = request.json.get('price')
        delivery_type = request.json.get('delivery_type')
        size_id = request.json.get('size_id')
        print(price, delivery_type, size_id)

        try:
            if delivery_type or delivery_type == 0:
                if 0 <= delivery_type <= 1:
                    delivery_type = DELIVERY_TYPE[delivery_type]
                else:
                    return jsonify({'result': "추가 실패 - 올바른 배송 종류를 선택하세요."})

            stock = Stock(price=price, delivery_type=delivery_type, size_id=size_id)

            db.session.add(stock)
            db.session.commit()

            result = make_result(stock)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Stock_api.route('/<int:id>')
@Stock_api.doc(params={'id': 'Stock ID'})
class StockRUD(Resource):
    def get(self, id):
        """
          Get a stock with ID.
        """
        """
          Request:
            GET /stocks/1
          Returns:
            {
              "id": 1,
              "price": 89000,
              "delivery_type": "빠른 배송",
              "status": false,
              "purchased_at": null,
              "size_id": 1
            }
        """
        print(id)

        try:
            stock = db.session.get(Stock, id)

            result = make_result(stock)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update a stock.
        """
        """
          Request:
            PATCH /stocks/1
            {
              "delivery_type": 1,
              "status": true,
              "purchased_at": "2024-05-15"
            }
          Returns:
            {
              "id": 1,
              "price": 89000,
              "delivery_type": "일반 배송",
              "status": true,
              "purchased_at": "2024-05-15",
              "size_id": 1
            }
        """
        price = request.json.get('price')
        delivery_type = request.json.get('delivery_type')
        status = request.json.get('status')
        purchased_at = request.json.get('purchased_at')
        size_id = request.json.get('size_id')
        print(id, price, delivery_type, status, purchased_at, size_id)

        try:
            stock = db.session.get(Stock, id)

            if price:
                stock.price = price

            if delivery_type or delivery_type == 0:
                if 0 <= delivery_type <= 1:
                    stock.delivery_type = DELIVERY_TYPE[delivery_type]
                else:
                    return jsonify({'result': "수정 실패 - 올바른 배송 종류를 선택하세요."})

            if status:
                stock.status = status
            if purchased_at:
                stock.purchased_at = datetime.strptime(purchased_at, '%Y-%m-%d')
            if size_id:
                stock.size_id = size_id

            db.session.commit()

            result = make_result(stock)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete a stock.
        """
        """
          Request:
            DELETE /stocks/3
          Returns:
            {}
        """
        print(id)

        try:
            stock = db.session.get(Stock, id)

            db.session.delete(stock)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(stock):
    purchased_at = stock.purchased_at
    if purchased_at:
        purchased_at = purchased_at.strftime('%Y-%m-%d')

    result = {
        'id': stock.id,
        'price': stock.price,
        'delivery_type': stock.delivery_type,
        'status': not not stock.status,
        'purchased_at': purchased_at,
        'size_id': stock.size_id
    }

    return result
