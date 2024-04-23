from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer

ma = Marshmallow()

class FlavorsResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    created_at = String(required=True, dump_only=True)
    flavor_id = String(required=True, dump_only=True)
    ram = Integer(required=True, dump_only=True)
    vcpus = Integer(required=True, dump_only=True)
    is_public = String(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    is_disabled = String(required=True, dump_only=True)