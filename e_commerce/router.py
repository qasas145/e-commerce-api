from flask_restx import Namespace
import sqlalchemy
com = Namespace("e-commerce", description="an api for e-commerce")

from .views import CategoryView, CustomerView, OrderView, ProductView

com.add_resource(CategoryView, "/category/")
com.add_resource(ProductView, "/product/")
com.add_resource(CustomerView, "/customer/")
com.add_resource(OrderView, "/order/")
