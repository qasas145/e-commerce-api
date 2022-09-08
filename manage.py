from flask_restx import Api
from flask import Flask
from db import db
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from user.router import user_ns
from authorization import authorizations
# from posts.router import post_ns
from e_commerce.router import com



app = Flask(__name__, static_url_path='', static_folder='')

# CORS(app)

base_dir = os.path.dirname(os.path.realpath(__file__))

app.config['SECRET_KEY'] = 'mohamed sayed'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'databases/data.db')
app.config['SQLALCHEMY_ECHO'] = True


JWTManager(app)

db.init_app(app)


migrate = Migrate(app, db)

api = Api(app, doc='/api',authorizations=authorizations, description="This an api for important news")
# api.add_namespace(user_ns)
# api.add_namespace(post_ns)
api.add_namespace(com)