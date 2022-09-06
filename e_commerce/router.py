from flask_restx import Namespace
import sqlalchemy
com = Namespace("e-commerce", description="an api for e-commerce")

from .views import CategoryView, ProductView

com.add_resource(CategoryView, "/category/")
com.add_resource(ProductView, "/product/")
