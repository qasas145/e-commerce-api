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