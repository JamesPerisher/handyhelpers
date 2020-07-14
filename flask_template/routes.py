from flask import Blueprint
import activity


routes = Blueprint("routes", __name__)
activity.routes = routes

@routes.record
def record(state):
    routes.db = state.app.config.get("database")

    if routes.db is None:
        raise Exception("This blueprint expects you to provide database access through database")


routes.route("/", methods=["GET"])(activity.home)
routes.errorhandler(Exception)(activity.error)
