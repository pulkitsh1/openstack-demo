from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer

ma = Marshmallow()

class InstanceResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    created_at = String(required=True, dump_only=True)
    image_id = Integer(required=True, dump_only=True)
    flavor_id = Integer(required=True, dump_only=True)
    status = String(required=True, dump_only=True)