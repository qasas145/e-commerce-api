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
        if kwargs.get("name", None) : self.name = kwargs.get("name")
        if kwargs.get("price", None) : self.price = kwargs.get("price")
        if kwargs.get("category_id", None) : self.category_id = kwargs.get("category_id")
        if kwargs.get("description", None) : self.description = kwargs.get("description")
        if kwargs.get("image", None) : self.image = generate_password_hash(kwargs.get("image"))
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
        if kwargs.get("first_name", None) : self.first_name = kwargs.get("first_name")
        if kwargs.get("last_name", None) : self.last_name = kwargs.get("last_name")
        if kwargs.get("phone", None) : self.phone = kwargs.get("phone")
        if kwargs.get("email", None) : self.email = kwargs.get("email")
        if kwargs.get("password", None) : self.password = generate_password_hash(kwargs.get("password"))
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
        if kwargs.get("customer_id", None) : self.customer_id = kwargs.get("customer_id")
        if kwargs.get("address", None) : self.address = kwargs.get("address")
        if kwargs.get("quantity", None) : self.quantity = kwargs.get("quantity")
        if kwargs.get("status", None) : self.status = kwargs.get("status")
        db.session.commit()
    def __repr__(self) -> str:
        return f'{self.customer_id} - {self.address}'