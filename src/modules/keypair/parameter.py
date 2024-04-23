from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer
from marshmallow import validate, validates_schema, ValidationError

ma = Marshmallow()

class create_keypair(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)


class delete_keypair(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)

