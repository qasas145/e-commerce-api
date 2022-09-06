from .router import user_ns
from flask_restx import fields



UserSerializer = user_ns.model(
    "User" ,{
        "id" : fields.Integer(),
        "email" : fields.String()
    }
)
