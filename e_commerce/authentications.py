from flask_restx import Resource
from flask import request, jsonify, make_response
from .models import Customer
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
from http import HTTPStatus


class LoginView(Resource) :
    from .router import com
    @com.doc(params={
        "email" : {'in' : 'query', 'description' : 'user email', 'required' : True},
        'password' : {'in' : 'query', 'required' : True, 'description' : 'user password'}
    })
    def post(self) :
        email = request.args.get("email")
        customer = Customer.query.filter_by(email = email).first()
        if customer :
            password = request.args.get("password")
            if check_password_hash(customer.password, password):
                access_token = create_access_token(identity=customer.id, expires_delta=timedelta(hours=5))
                refresh_token = create_refresh_token(identity=customer.id, expires_delta=timedelta(days=2))
                print("hello")
                return jsonify({"access_token":access_token, "refresh_token" : refresh_token, "how_to_use":"Enter token on the pattern :Bearer <token>"})
            return make_response({'message' : 'Invalid password'}, HTTPStatus.BAD_REQUEST)
        return make_response({'message' : 'Invalid username'}, HTTPStatus.BAD_REQUEST)
