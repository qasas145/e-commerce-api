import json
from db import db
from flask import jsonify, request, make_response
from .permissions import IsAuthenticatedOReadOnly
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from flask_restx import Resource, marshal
from .models import Category, Customer, Order, Product
from .serializer import CategorySerializer, CustomerSerializer, OrderSerializer, ProductSerializer
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash




class CategoryView(Resource) :
    from .router import com
    @com.marshal_list_with(CategorySerializer)
    def get(self) :
        return Category.get_all_categories()
    @com.doc(params={"name" : {"in" : 'query', 'description' : 'Name of category', 'required' : True}})    
    @com.marshal_with(CategorySerializer)
    def post(self) :
        data = request.args
        new_category = Category(**data)
        new_category.save()
        return new_category



class CategoryViewPk(Resource) :
    from .router import com
    @com.marshal_with(CategorySerializer)
    def get(self, id) :
        return Category.query.get_or_404(id)
    @com.doc(params={"name" : {"in" : 'query', 'description' : 'Name of category'}})   
    @com.marshal_with(CategorySerializer)
    def put(self, id) :
        data = request.args
        category = Category.query.get_or_404(id)
        category.update(**data)
        return category
    def delete(self, id) :
        category = Category.query.get_or_404(id)
        category.delete()
        return jsonify({'details' : 'deleted .'})




class ProductView(Resource) :
    from .router import com
    @com.marshal_list_with(ProductSerializer)
    def get(self) :
        return Product.get_product_by_id(None)
    parser = com.parser()
    parser.add_argument("name", type='str', required = True)
    parser.add_argument("price", type=int, required = True)
    parser.add_argument("category_id", type=int, required = True)
    parser.add_argument('description', type=str, required = True)
    parser.add_argument("image", type=FileStorage, location="files", required = True)
    @com.expect(parser)
    @com.marshal_with(ProductSerializer)
    def post(self) :
        image = request.files.get('image', None)
        new_product = Product(**request.args, image=image.read())
        new_product.save()
        return new_product




class ProductViewPk(Resource) :
    from .router import com
    @com.marshal_with(ProductSerializer)
    def get(self, id) :
        return Product.get_product_by_id(id)
    parser = com.parser()
    parser.add_argument("name", type=str)
    parser.add_argument("price", type=int)
    parser.add_argument("category_id", type=int)
    parser.add_argument('description', type=str)
    parser.add_argument("image", type=FileStorage, location="files")
    @com.expect(parser)
    @com.marshal_with(ProductSerializer)
    def put(self, id) :
        image = request.files.get('image', None)
        product = Product.get_product_by_id(id)
        if image :
            product.update(**request.args, image=image.read())
        else :
            product.update(**request.args)
        return product
    def delete(self, id) :
        product = Product.get_product_by_id(id)
        product.delete()
        return jsonify({'details' : 'deleted .'})




class CustomerView(Resource) :
    from .router import com
    @com.marshal_list_with(CustomerSerializer)
    def get(self) :
        return Customer.query.all()
    
    @com.doc(params={
        "first_name" : {'in' : 'query', 'required' : True},
        "last_name" : {'in' : 'query', 'required' : True},
        'phone' : {'in' : 'query', 'type' :'integer', 'required' : True},
        'email' : {'in' : 'query', 'type' : 'string', 'required' : True},
        'password' : {'in' : 'query', 'required' : True},
    })
    def post(self) :

        try :
            request.args._mutable = True
        except :
            pass
        data = request.args
        new_customer = Customer(**data)
        if new_customer.isExists() :
            return make_response({'details .' : "email is already exists ."})
        new_customer.password = generate_password_hash(new_customer.password)
        new_customer.save()
        return marshal(new_customer, CustomerSerializer)




class CustomerViewPk(Resource) :
    from .router import com
    @com.marshal_with(CustomerSerializer)
    def get(self, id) :
        return Customer.query.get_or_404(id)
    
    @com.doc(params={
        "first_name" : {'in' : 'query'},
        "last_name" : {'in' : 'query'},
        'phone' : {'in' : 'query', 'type' :'integer'},
        'email' : {'in' : 'query', 'type' : 'string'},
        'password' : {'in' : 'query'},
    })
    @com.doc(security="apikey")
    @jwt_required()
    def put(self, id) :
        permission_class = IsAuthenticatedOReadOnly().__repr__(get_jwt_identity(), id)
        if  permission_class != True:
            return permission_class
        data = request.args
        if data.get("email", None) :
            if Customer.get_customer_by_email(email=data.get("email")) :
                return make_response({'details .' : "email is already exists ."})
        customer = Customer.query.get_or_404(id)
        customer.update(**data)
        return marshal(customer, CustomerSerializer)
    @com.doc(security="apikey")
    @jwt_required()
    def delete(self, id) :
        permission_class = IsAuthenticatedOReadOnly().__repr__(get_jwt_identity(), id)
        if  permission_class != True:
            return permission_class
        customer = Customer.query.get_or_404(id)
        customer.delete()
        return jsonify({'details' : 'deleted .'})




class OrderView(Resource) :
    from .router import com
    @com.marshal_list_with(OrderSerializer)
    def get(self) :
        return Order.query.all()
    
    @com.doc(params={
        "product_id" : {'in' : 'query', 'type' : 'integer', 'required' : True},
        "customer_id" : {'in' : 'query', 'type' : 'integer', 'required' : True},
        'quantity' : {'in' : 'query', 'type' :'integer', 'required' : True},
        'address' : {'in' : 'query', 'type' : 'string', 'required' : True},
        'phone' : {'in' : 'query', 'type' : 'integer', 'required' : True},
        'status' : {'in' : 'query', 'type' : 'boolean', 'required' : True}
    })
    @com.marshal_with(OrderSerializer)
    def post(self) :
        data = request.args
        new_order = Order(**data)
        if new_order.status == 'true' :
            new_order.status=1
        else : new_order.status=0
        new_order.save()
        return new_order




class OrderViewPk(Resource) :
    from .router import com
    @com.marshal_with(OrderSerializer)
    def get(self, id) :
        return Order.query.get_or_404(id)
    def delete(self, id) :
        order = Order.query.get_or_404(id)
        order.delete()
        return jsonify({'details' : 'deleted .'})
    @com.marshal_with(OrderSerializer)
    @com.doc(params={
        "product_id" : {'in' : 'query', 'type' : 'integer'},
        "customer_id" : {'in' : 'query', 'type' : 'integer'},
        'quantity' : {'in' : 'query', 'type' :'integer'},
        'address' : {'in' : 'query', 'type' : 'string'},
        'phone' : {'in' : 'query', 'type' : 'integer'},
        'status' : {'in' : 'query', 'type' : 'boolean'}
    })
    def put(self, id) :
        data = request.args
        order = Order.query.get_or_404(id)
        order.update(**data)
        return order