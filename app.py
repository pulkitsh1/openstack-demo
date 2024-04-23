from flask import Flask
from flask_smorest import Api
import config
from flask_migrate import Migrate
from src.service_modules.db.conn import db
from src.modules.flavors.endpoints import api as flavors_api
from src.modules.images.endpoints import api as images_api
from src.modules.instances.endpoints import api as instances_api
from src.modules.networks.endpoints import api as networks_api
from src.modules.volumes.endpoints import api as volumes_api
from src.modules.keypair.endpoints import api as keypair_api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQL_CONNECTION
app.config['API_TITLE'] = "Openstack API's"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

blplist = [flavors_api, images_api, instances_api, networks_api, volumes_api, keypair_api]
for blp in blplist:
    api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(debug=True)