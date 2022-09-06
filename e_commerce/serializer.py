from .router import com
from flask_restx import fields

CategorySerializer = com.model(
    "Category",
    {
        "id" : fields.Integer(),
        "name" : fields.String(),
    }
)

ProductSerializer = com.model(
    "Product",
    {
        "id" : fields.Integer(),
        "name" : fields.String(),
        "category_id" : fields.Integer(),
        "price" : fields.Integer(),
        "description" : fields.String(),
    }
)

CustomerSerializer = com.model(
    "Customer",
    {
        "id" : fields.Integer(),
        "first_name" : fields.String(),
        "last_name" : fields.String(),
        "phone" : fields.Integer(),
        "email" : fields.String()
    }
)

OrderSerializer = com.model(
    "Order",
    {
        "id" : fields.Integer(),
        "product_id" : fields.Integer(),
        "customer_id" : fields.Integer(),
        "quantity" : fields.Integer(),
        "address" : fields.String(),
        "date" : fields.Date()
    }
)