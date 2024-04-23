from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
import logging, json
from http import HTTPStatus
from src.service_modules.openstack.conn import conn
from src.service_modules.db.conn import db
from src.modules.networks.parameter import create_network, delete_network
from src.modules.networks.models import Network, Subnet
from src.modules.networks.response import NetworkResponse

api = Blueprint("networks",__name__)

@api.route('/networks')
class networks(MethodView):

    @api.response(HTTPStatus.OK,schema=NetworkResponse(many=True))
    def get(self):
        try:
            res = Network.query.all()
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
            
    @api.arguments(schema=create_network())
    def post(self, req_data):
        try:
            network = conn.network.create_network(
                name= req_data.get('network_name')
            )

            subnet = conn.network.create_subnet(
                name=req_data.get('subnet_name'),
                network_id=network.id,
                ip_version=int(req_data.get('ip_version')),
                cidr=req_data.get('cidr'),
                gateway_ip=req_data.get('gateway_ip'),
                )

            entry = Network(name=req_data.get('network_name'), network_id=network.get('id'), created_at=network.get('created_at'), status =req_data.get('status'))
            entry2 = Subnet(name=req_data.get('subnet_name'), ip_version=req_data.get('ip_version'), cidr=req_data.get('cidr'),gateway_ip=req_data.get('gateway_ip'),network=entry, status =req_data.get('status'))
            db.session.add(entry)
            db.session.add(entry2)
            db.session.commit()
            return {"message":"Network created successfully.","status": HTTPStatus.OK}
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

    @api.arguments(schema=delete_network())
    def delete(self, req_data):
        try:
            network = conn.network.find_network(
                req_data.get('network_id')
            )

            if network:
                for subnet in network.subnet_ids:
                    conn.network.delete_subnet(subnet, ignore_missing=False)

                conn.network.delete_network(network, ignore_missing=False)

                network_info = Network.query.filter_by(network_id=req_data.get('network_id')).first()
                network_info.status = 'deleted'
                subnet_info = network_info.subnets
                for subnet in subnet_info:
                    subnet.status = 'deleted'
                db.session.commit()
            else:
                raise Exception("No network exists by this id.",HTTPStatus.NOT_FOUND)

            return {"message":"Network deleted successfully.","status": HTTPStatus.OK}
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
