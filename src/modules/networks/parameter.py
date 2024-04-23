from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer
from marshmallow import validate, validates_schema, ValidationError

ma = Marshmallow()

class create_network(ma.SQLAlchemyAutoSchema):
    network_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    subnet_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    cidr = String(required=True, load_only=True)
    ip_version = Integer(required=False, load_only=True)
    gateway_ip = String(required=False, load_only=True)
    status = String(required=False, load_only=True)

class delete_network(ma.SQLAlchemyAutoSchema):
    network_id = String(required=True,validate=[validate.Length(min=3)], load_only=True)

