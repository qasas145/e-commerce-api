from flask import jsonify, request
from flask_cors import cross_origin
from flask_restx import Resource
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
        print(request.args)
        image = request.files.get('image', None)
        new_product = Product(**request.args, image=image.read())
        new_product.save()
        return new_product




class CustomerView(Resource) :
    from .router import com
    @com.marshal_list_with(CustomerSerializer)
    def get(self) :
        return Customer.query.all()
    
    @com.doc(params={
        "first_name" : {'in' : 'query', 'required' : True},
        "last_name" : {'in' : 'query'},
        'phone' : {'in' : 'query', 'type' :'integer', 'required' : True},
        'email' : {'in' : 'query', 'type' : 'string', 'required' : True},
        'password' : {'in' : 'query', 'required' : True},
    })
    @com.marshal_with(CustomerSerializer)
    def post(self) :

        try :
            request.args._mutable = True
        except :
            pass
        data = request.args
        new_customer = Customer(**data)
        new_customer.password = generate_password_hash(new_customer.password)
        new_customer.save()
        return new_customer




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