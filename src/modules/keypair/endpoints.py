from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
import logging, json
from http import HTTPStatus
from src.service_modules.openstack.conn import conn
from src.service_modules.db.conn import db
from src.modules.keypair.models import KeyPair
from src.modules.keypair.response import KeyPairResponse
from src.modules.keypair.parameter import create_keypair, delete_keypair

api = Blueprint("keypairs",__name__)

@api.route('/keypairs')
class keypair(MethodView):

    @api.response(HTTPStatus.OK,schema=KeyPairResponse(many=True))
    def get(self):
        try:
            res = KeyPair.query.all()
            return res
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

    @api.arguments(schema=create_keypair())
    def post(self, req_data):
        try:
            keypair = conn.compute.create_keypair(name=req_data.get('name'))

            if keypair:
                entry = KeyPair(name=req_data.get('name'), private_key=keypair.get('private_key'), fingerprint=keypair.get('fingerprint'),type=keypair.get('type'),public_key=keypair.get('public_key'), status ='Active')
                db.session.add(entry)
                db.session.commit()
            return {"message":"Key-Pair created successfully.","status": HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

    @api.arguments(schema=delete_keypair())
    def delete(self, req_data):
        try:
            keypair = conn.compute.get_keypair(req_data.get('name'))
            if keypair:
                conn.compute.delete_keypair(keypair)

                network_info = KeyPair.query.filter_by(name=req_data.get('name')).first()
                network_info.status = 'deleted'
                db.session.commit()
            else:
                raise Exception("No Key-pair exists by this id.",HTTPStatus.NOT_FOUND)

            return {"message":"Key-Pair deleted successfully.","status": HTTPStatus.OK}
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))