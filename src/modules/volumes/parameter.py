from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer
from marshmallow import validate, validates_schema, ValidationError

ma = Marshmallow()

class create_volume(ma.SQLAlchemyAutoSchema):
    volume_name = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    volume_size = Integer(required=True, load_only=True)
    description = String(required=True, load_only=True)
    volume_type = String(required=False, load_only=True)
    availabity_zone = String(required=False, load_only=True)
    status = String(required=True, load_only=True)

class delete_volume(ma.SQLAlchemyAutoSchema):
    volume_id = String(required=True, load_only=True)
    
class resize_volume(ma.SQLAlchemyAutoSchema):
    volume_id = String(required=True, load_only=True)
    size = Integer(required=True, load_only=True)