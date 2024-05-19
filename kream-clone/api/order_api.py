from datetime import datetime

from flask import request, jsonify
from flask_restx import Namespace, Resource

from config import DELIVERY_TYPE, DELIVERY_TYPE_PRICE, ORDER_STATUS
from models import Order, db, Stock, Size, Item
from my_jwt import validate_token, get_user_id

Order_api = Namespace(name='Order_api', description="API for managing orders")


@Order_api.route('')
class OrderCR(Resource):
    def get(self):
        """
          Get all orders with jwt.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "ordered_at": "24/05/19 21:24",
                "stock_id": 1,
                "price": 94000,
                "status": "발송완료",
                "delivery_id": 1,
                "user_id": 1
              },
              {
                "id": 2,
                "ordered_at": "24/05/19 21:28",
                "stock_id": 5,
                "price": 107000,
                "status": null,
                "delivery_id": 3,
                "user_id": 1
              },
              ...
            ]
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id)

        result = []

        try:
            orders = Order.query.filter_by(user_id=user_id).all()

            for order in orders:
                result.append(make_result(order))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new order.
          Update a stock.
          Update an item.
        """
        """
          Request:
            {
              "stock_id": 1,
              "delivery_id": 1
            }
          Returns:
            {
              "id": 1,
              "ordered_at": "24/05/19 21:24",
              "stock_id": 1,
              "price": 94000,
              "status": null,
              "delivery_id": 1,
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)

        stock_id = request.json.get('stock_id')
        delivery_id = request.json.get('delivery_id')
        print(user_id, stock_id, delivery_id)

        try:
            stock = db.session.get(Stock, stock_id)
            price = stock.price
            delivery_type = stock.delivery_type

            for i in range(len(DELIVERY_TYPE)):
                if delivery_type == DELIVERY_TYPE[i]:
                    price += DELIVERY_TYPE_PRICE[i]

            order = Order(stock_id=stock_id, ordered_at=datetime.now(), price=price, delivery_id=delivery_id, user_id=user_id)
            db.session.add(order)

            stock.status = True
            stock.purchased_at = order.ordered_at.date()

            size = db.session.get(Size, stock.size_id)
            item = db.session.get(Item, size.item_id)
            item.transaction_number += 1

            db.session.commit()

            result = make_result(order)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Order_api.route('/<int:id>')
@Order_api.doc(params={'id': 'Order ID'})
class OrderRUD(Resource):
    def get(self, id):
        """
          Get an order with ID.
        """
        """
          Request:
            GET /orders/1
          Returns:
            {
              "id": 1,
              "ordered_at": "24/05/19 21:24",
              "stock_id": 1,
              "price": 94000,
              "status": "발송완료",
              "delivery_id": 1,
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            order = db.session.get(Order, id)

            if order.user_id != user_id:
                return jsonify({'result': "조회 실패 - 권한 없음"})

            result = make_result(order)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def patch(self, id):
        """
          Update an order.
        """
        """
          Request:
            PATCH /orders/1
            {
              "status": 0
            }
          Returns:
            {
              "id": 1,
              "ordered_at": "24/05/19 21:24",
              "stock_id": 1,
              "price": 94000,
              "status": "발송완료",
              "delivery_id": 1,
              "user_id": 1
            }
        """
        status = request.json.get('status')
        print(id, status)

        try:
            order = db.session.get(Order, id)

            if 0 <= status < len(ORDER_STATUS):
                order.status = ORDER_STATUS[status]

                db.session.commit()

                result = make_result(order)

            else:
                result = {'result': "수정 실패 - 올바른 진행 상황을 선택하세요."}

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete an order.
          Update a stock.
          Update an item.
        """
        """
          Request:
            DELETE /orders/1
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            order = db.session.get(Order, id)

            if order.user_id != user_id:
                return jsonify({'result': "삭제 실패 - 권한 없음"})

            stock = db.session.get(Stock, order.stock_id)

            stock.status = False
            stock.purchased_at = None

            size = db.session.get(Size, stock.size_id)
            item = db.session.get(Item, size.item_id)
            item.transaction_number -= 1

            db.session.delete(order)
            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(order):
    result = {
        'id': order.id,
        'ordered_at': order.ordered_at.strftime('%y/%m/%d %H:%M'),
        'stock_id': order.stock_id,
        'price': order.price,
        'status': order.status,
        'delivery_id': order.delivery_id,
        'user_id': order.user_id
    }

    return result
