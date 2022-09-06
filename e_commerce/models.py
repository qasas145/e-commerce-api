from datetime import datetime
from db import db


class Product(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    price = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    description = db.Column(db.String(250), default='', nullable = True)
    image = db.Column(db.BLOB)
    orders = db.relationship("Order", backref="product")

    @staticmethod
    def get_product_by_id(id):
        if id :
            return Product.query.get_or_404(id)
        return Product.query.all()
    
    def save(self) :
        db.session.add(self)
        db.session.commit()

   
class Category(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    products = db.relationship("Product", backref="category")


    @staticmethod
    def get_all_categories() :
        return Category.query.all()
    
    def save(self) :
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return self.name

    
class Customer(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100))
    orders = db.relationship("Order", backref="customer")

    @staticmethod
    def get_customer_by_email(email) :
        try :
            return Customer.query.filter_by(email = email)
        except :
            return None
    def isExists(self) :
        if Customer.query.filter_by(email = self.email) :
            return True
        return False

class Order(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    quantity = db.Column(db.Integer)
    address = db.Column(db.String(50), default='', nullable = True)
    phone = db.Column(db.String(11), nullable = True)
    date = db.Column(db.Date, default=datetime.today)
    status = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_orders_by_customer(customer_id) :
        return Order.query.filter_by(customer = customer_id).order_by(Order.date.desc())
 
