from http import HTTPStatus

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from backend.db import db_session
from backend.errors import AppError
from backend.views import images, tasks, upload


def shutdown_session(exception=None):
    db_session.remove()


def handle_http_exceptions(error: HTTPException):
    return {'message': error.description}, error.code


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


def create_app():

    app = Flask(__name__)

    app.register_blueprint(upload.view, url_prefix='/api/v1/upload')
    app.register_blueprint(images.view, url_prefix='/api/v1/images')
    app.register_blueprint(tasks.view, url_prefix='/api/v1/tasks')

    app.register_error_handler(HTTPException, handle_http_exceptions)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    app.teardown_appcontext(shutdown_session)

    return app
