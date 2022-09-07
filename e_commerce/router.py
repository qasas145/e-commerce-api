from flask_restx import Namespace
import sqlalchemy
com = Namespace("e-commerce", description="an api for e-commerce")

from .views import CategoryView, CategoryViewPk, CustomerView, CustomerViewPk, OrderView, OrderViewPk, ProductView, ProductViewPk

com.add_resource(CategoryView, "/category/")
com.add_resource(CategoryViewPk, "/category/<int:id>")
com.add_resource(ProductView, "/product/")
com.add_resource(ProductViewPk, "/product/<int:id>")
com.add_resource(CustomerView, "/customer/")
com.add_resource(CustomerViewPk, "/customer/<int:id>")
com.add_resource(OrderView, "/order/")
com.add_resource(OrderViewPk, "/order/<int:id>")
