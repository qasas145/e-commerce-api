from flask import jsonify, request
from flask_cors import cross_origin
from flask_restx import Resource
from .models import Category, Customer, Order, Product
from .serializer import CategorySerializer, ProductSerializer
from werkzeug.datastructures import FileStorage


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

