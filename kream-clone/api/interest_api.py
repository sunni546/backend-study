from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import Interest, db, Size, Item
from my_jwt import validate_token, get_user_id

Interest_api = Namespace(name='Interest_api', description="API for managing interests")


@Interest_api.route('')
class InterestCR(Resource):
    def get(self):
        """
          Get all interests with jwt.
        """
        """
          Returns:
            [
              {
                "id": 1,
                "size_id": 1,
                "user_id": 1
              },
              {
                "id": 2,
                "size_id": 4,
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
            interests = Interest.query.filter_by(user_id=user_id).all()

            for interest in interests:
                result.append(make_result(interest))

        except Exception as e:
            print(e)

        return jsonify(result)

    def post(self):
        """
          Create a new interest.
          Update an item.
        """
        """
          Request:
            {
              "size_id": 1
            }
          Returns:
            {
              "id": 1,
              "size_id": 1,
              "user_id": 1
            }
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        size_id = request.json.get('size_id')
        print(user_id, size_id)

        try:
            interest = Interest.query.filter_by(size_id=size_id, user_id=user_id).first()
            if interest:
                result = {'result': "관심상품 추가 실패 - 이미 사용자가 관심 추가한 상품입니다."}

            else:
                interest = Interest(size_id=size_id, user_id=user_id)
                db.session.add(interest)

                size = Size.query.filter_by(id=size_id).with_entities(Size.item_id).first()
                item = db.session.get(Item, size.item_id)
                item.interest_number += 1

                db.session.commit()

                result = make_result(interest)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)


@Interest_api.route('/<int:id>')
@Interest_api.doc(params={'id': 'Interest ID'})
class InterestRD(Resource):
    def get(self, id):
        """
          Get an interest with ID.
        """
        """
          Request:
            GET /interests/1
          Returns:
            {
              "id": 1,
              "size_id": 1,
              "user_id": 1
            }
        """
        print(id)

        try:
            interest = db.session.get(Interest, id)

            result = make_result(interest)

        except Exception as e:
            print(e)
            result = {}

        return jsonify(result)

    def delete(self, id):
        """
          Delete an interest.
          Update an item.
        """
        """
          Request:
            DELETE /interests/3
          Returns:
            {}
        """
        token = request.headers.get('Authorization')

        if not validate_token(token):
            return jsonify({'result': "로그인 실패"})

        user_id = get_user_id(token)
        print(user_id, id)

        try:
            interest = db.session.get(Interest, id)

            if interest.user_id != user_id:
                return jsonify({'result': "삭제 실패 - 권한 없음"})

            db.session.delete(interest)

            size = Size.query.filter_by(id=interest.size_id).with_entities(Size.item_id).first()
            item = db.session.get(Item, size.item_id)
            item.interest_number -= 1

            db.session.commit()

            result = {}

        except Exception as e:
            print(e)
            result = {'result': "삭제 실패"}

        return jsonify(result)


def make_result(interest):
    result = {
        'id': interest.id,
        'size_id': interest.size_id,
        'user_id': interest.user_id
    }

    return result
