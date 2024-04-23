from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
import logging, json
from http import HTTPStatus
from src.service_modules.openstack.conn import conn
from src.service_modules.db.conn import db
from src.modules.instances.parameter import create_instance, delete_instance, attach_interface
from src.modules.instances.response import InstanceResponse
from src.modules.instances.models import Instances
from src.modules.images.models import Images
from src.modules.flavors.models import Flavors
from src.modules.networks.models import Network
from src.modules.keypair.models import KeyPair

api = Blueprint("instances",__name__)

@api.route('/instances')
class instances(MethodView):

    @api.response(HTTPStatus.OK,schema=InstanceResponse(many=True))
    def get(self):
        try:
            res = Instances.query.all()
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

    @api.arguments(schema=create_instance())
    def post(self, req_data):
        try:
            image = Images.query.filter_by(name = req_data.get('image_name')).first()
            flavor = Flavors.query.filter_by(name = req_data.get('flavor_name')).first()
            network = Network.query.filter_by(name = req_data.get('network_name')).first()
            keypair = KeyPair.query.filter_by(name = req_data.get('keypair_name')).first()

            server = conn.compute.create_server(
                name=req_data.get('server_name'),
                image_id=image.image_id,
                flavor_id=flavor.flavor_id,
                networks=[{"uuid": network.network_id}],
                key_name=keypair.name,
            )

            wait = conn.compute.wait_for_server(server)

            if server:
                entry = Instances(name=req_data.get('server_name'),created_at=server.created_at,network=network,images=image,flavors=flavor,key_pair=keypair,status=server.status)
                db.session.add(entry)
                db.session.commit()
                
            return {"message":"Instance created successfully.","status": HTTPStatus.OK}
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

    @api.arguments(schema=attach_interface())
    def put(self, req_data):
        try:
            instance = Instances.query.filter_by(req_data.get("instance_id")).first()

            port = conn.network.create_port(
                name=req_data.get("port_name"),
                network_id=req_data.get("network_id"),
                project_id=req_data.get("project_id")
            )

            conn.compute.attach_interface(
                server=instance.id,
                port_id=port.id
            )

            return {"message":"Interface attached to the given instance successfully.","status": HTTPStatus.OK}
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

    @api.arguments(schema=delete_instance())
    def delete(self, req_data):
        try:
            server = conn.compute.find_server(req_data.get('name'))
            if server:
                conn.compute.delete_server(server)

                instance_info = Instances.query.filter_by(name=req_data.get('name')).first()
                instance_info.status = 'DELETED'
                db.session.commit()
            else:
                raise Exception("No Instance exists by this name.",HTTPStatus.NOT_FOUND)

            return {"message":"Instance deleted successfully.","status": HTTPStatus.OK}
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

@api.route('/instances/<instance_id>/detach_interface/port/<port_id>')
class DetachInterface(MethodView):

    def put(self, instance_id,port_id):
        try:
            instance = Instances.query.filter_by(instance_id).first()

            conn.compute.detach_interface(
                server=instance.id,
                port_id=port_id
            )

            return {"message":"Interface detached from the given instance successfully.","status": HTTPStatus.OK}
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