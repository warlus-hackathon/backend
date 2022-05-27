from http import HTTPStatus

from flask import Blueprint

from backend import schemas
from backend.repo.images import Image

view = Blueprint('task', __name__)


task_repo = Image()


@view.get('/')
def get_task():
    entity = task_repo.get_not_recognized()
    image = schemas.Image.from_orm(entity)
    return image.dict(), HTTPStatus.OK
