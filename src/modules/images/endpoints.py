from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
import logging, json
from http import HTTPStatus
from src.modules.images.models import Images
from src.modules.images.response import ImageResponse

api = Blueprint("images",__name__)

@api.route('/images')
class images(MethodView):

    @api.response(HTTPStatus.OK,schema=ImageResponse(many=True))
    def get(self):
        try:
            res = Images.query.all()
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

