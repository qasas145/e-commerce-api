from flask_restx import fields, Namespace

user_ns = Namespace("user", description="an api for the users")

from .views import LoginView, SignUpView, UsersView

user_ns.add_resource(UsersView, "/users/")
user_ns.add_resource(SignUpView, "/signup/")
user_ns.add_resource(LoginView, "/login/")