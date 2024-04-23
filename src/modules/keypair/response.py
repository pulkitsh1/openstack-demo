from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer

ma = Marshmallow()

class KeyPairResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, dump_only=True)
    private_key = String(required=True, dump_only=True)
    fingerprint = String(required=True, dump_only=True)
    type = String(required=True, dump_only=True)
    public_key = String(required=True, dump_only=True)
    status = String(required=True, dump_only=True)