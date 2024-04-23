from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer
from marshmallow import validate, validates_schema, ValidationError

ma = Marshmallow()

class create_instance(ma.SQLAlchemyAutoSchema):
    image_name = String(required=True, load_only=True) 
    flavor_name = String(required=True, load_only=True)
    network_name = String(required=True, load_only=True)
    keypair_name = String(required=True, load_only=True)
    server_name = String(required=True, load_only=True)

class attach_interface(ma.SQLAlchemyAutoSchema):
    port_name = String(required=True, load_only=True)
    instance_id = Integer(required=True, load_only=True)
    network_id = Integer(required=True, load_only=True)
    project_id = Integer(required=True, load_only=True)

class delete_instance(ma.SQLAlchemyAutoSchema):
    name = String(required=True, load_only=True)