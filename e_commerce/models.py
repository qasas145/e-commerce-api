from datetime import datetime
from werkzeug.security import generate_password_hash
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
    def delete(self) :
        db.session.delete(self)
        db.session.commit()
    
    def update(self, *args, **kwargs) :
        if kwargs.get("name", None) : self.product_id = kwargs.get("name")
        if kwargs.get("price", None) : self.product_id = kwargs.get("price")
        if kwargs.get("category_id", None) : self.product_id = kwargs.get("category_id")
        if kwargs.get("description", None) : self.product_id = kwargs.get("description")
        if kwargs.get("image", None) : self.product_id = generate_password_hash(kwargs.get("image"))
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

    def delete(self) :
        db.session.delete(self)
        db.session.commit()
    def update(self, *args, **kwargs) :
        if kwargs.get("name", None) : self.product_id = kwargs.get("name")
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
    def save(self) :
        db.session.add(self)
        db.session.commit()
    
    def delete(self) :
        db.session.delete(self)
        db.session.commit()
    def update(self, *args, **kwargs) :
        if kwargs.get("first_name", None) : self.product_id = kwargs.get("first_name")
        if kwargs.get("last_name", None) : self.product_id = kwargs.get("last_name")
        if kwargs.get("phone", None) : self.product_id = kwargs.get("phone")
        if kwargs.get("email", None) : self.product_id = kwargs.get("email")
        if kwargs.get("password", None) : self.product_id = generate_password_hash(kwargs.get("password"))
        db.session.commit()
    def __repr__(self) -> str:
        return self.email

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
 
    def save(self) :
        db.session.add(self)
        db.session.commit()
    
    def delete(self) :
        db.session.delete(self)
        db.session.commit()
    def update(self, *args, **kwargs) :
        if kwargs.get("product_id", None) : self.product_id = kwargs.get("product_id")
        if kwargs.get("customer_id", None) : self.product_id = kwargs.get("customer_id")
        if kwargs.get("address", None) : self.product_id = kwargs.get("address")
        if kwargs.get("quantity", None) : self.product_id = kwargs.get("quantity")
        if kwargs.get("address", None) : self.product_id = kwargs.get("address")
        if kwargs.get("status", None) : self.product_id = kwargs.get("status")
        db.session.commit()
    def __repr__(self) -> str:
        return f'{self.customer_id} - {self.address}'