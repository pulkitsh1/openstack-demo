from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
import logging, json
from http import HTTPStatus
from src.service_modules.openstack.conn import conn
from src.service_modules.db.conn import db
from src.modules.volumes.models import Volume
from src.modules.volumes.response import VolumeResponse
from src.modules.volumes.parameter import create_volume, delete_volume, resize_volume

api = Blueprint("volumes",__name__)

@api.route('/volumes')
class volumes(MethodView):

    @api.response(HTTPStatus.OK,schema=VolumeResponse(many=True))
    def get(self):
        try:
            res = Volume.query.all()
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

    @api.arguments(schema=create_volume())
    def post(self, req_data):
        try:
            volume = conn.block_storage.create_volume(
                name=req_data.get('volume_name'),
                size=req_data.get('volume_size'),
                description=req_data.get('description'),
                volume_type=req_data.get('volume_type'),
                availability_zone=req_data.get('availabity_zone')
            )

            volume = conn.block_storage.wait_for_status(volume, status=req_data.get('status'))
            
            entry = Volume(name=req_data.get('volume_name'), size=req_data.get('volume_size'), description=req_data.get('description'), created_at=volume.get('created_at'), volume_id= volume.get('id'), status =req_data.get('status'))
            db.session.add(entry)
            db.session.commit()
            return {"message":"Volume created successfully.","status": HTTPStatus.OK}
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

    @api.arguments(schema=resize_volume())
    def put(self, req_data):
        try:
            volume_id = req_data.get('volume_id')
            volume_size = req_data.get('size')

            volume = conn.block_storage.find_volume(volume_id)

            if not volume:
                raise Exception("No volume exists by this id.",HTTPStatus.NOT_FOUND)

            conn.block_storage.extend_volume(volume,volume_size)

            volume_info = Volume.query.filter_by(volume_id=volume_id).first()

            volume_info.size = req_data.get('size')
            db.session.commit()

            return {"message":"Size of volume successfully updated.","status": HTTPStatus.OK}
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


    @api.arguments(schema=delete_volume())
    def delete(self, req_data):
        try:
            volume_id = req_data.get('volume_id')

            volume = conn.block_storage.get_volume(volume_id)

            if volume:
                conn.block_storage.delete_volume(volume)

                volume_info = Volume.query.filter_by(volume_id=volume_id).first()
                volume_info.status = 'deleted'
                db.session.commit()

                return {"message":"Volume deleted successfully.","status": HTTPStatus.OK}
            else:
                raise Exception(f"The volume id {volume_id} not found", HTTPStatus.NOT_FOUND)
            
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