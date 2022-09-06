from datetime import datetime, timedelta
from flask_restx import Resource
from flask import jsonify, request
from http import HTTPStatus
from .serializer import UserSerializer
from .models import User
from  werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required



class UsersView(Resource) :
    from .router import user_ns
    @user_ns.doc(security='apikey')
    @jwt_required()
    @user_ns.marshal_list_with(UserSerializer)
    def get(self) :
        users = User.query.all()
        return users, HTTPStatus.OK



class SignUpView(Resource) :
    from .router import user_ns
    @user_ns.marshal_with(UserSerializer)
    @user_ns.doc(params= {
    "email" : {'in' : 'query', 'description' : 'user email', 'required' : True},
    'password' : {'in' : 'query', 'required' : True, 'description' : 'user password'}
    })
    def post(self) :
        email = request.args.get("email")
        password = request.args.get("password")
        new_user = User(email = email, password = generate_password_hash(password))
        new_user.save()
        return new_user, HTTPStatus.CREATED


class LoginView(Resource) :
    from .router import user_ns
    @user_ns.doc(params={
        "email" : {'in' : 'query', 'description' : 'user email', 'required' : True},
        'password' : {'in' : 'query', 'required' : True, 'description' : 'user password'}
    })
    def post(self) :
        email = request.args.get("email")
        user = User.query.filter_by(email = email).first()
        if user :
            password = request.args.get("password")
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=5))
                refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=2))
                return jsonify(access_token=access_token, refresh_token = refresh_token)
            return jsonify({'message' : 'Invalid password'}), HTTPStatus.BAD_REQUEST
        return jsonify({'message' : 'Invalid username'}), HTTPStatus.BAD_REQUEST
