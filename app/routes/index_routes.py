from flask import Blueprint

index_routes = Blueprint("index_routes", __name__)


@index_routes.route("/")
@index_routes.route("/index")
def index():
    return "SQL more like sea quail amiright?"
