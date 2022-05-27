from http import HTTPStatus

from flask import Blueprint, request, jsonify

from backend import schemas
from backend.repo.images import Image

view = Blueprint('images', __name__)


image_repo = Image()


@view.post('/')
def add_image():
    image_info = request.json
    image_info['uid'] = -1
    image_info = schemas.Image(**image_info)

    entity = image_repo.add_images(image_info.name, image_info.path)
    new_image = schemas.Image.from_orm(entity)

    return new_image.dict(), HTTPStatus.CREATED


@view.get('/<uid>')
def get_image(uid):
    entity = image_repo.get_by_id(uid)
    image = schemas.Image.from_orm(entity)

    return image.dict(), HTTPStatus.OK


@view.get('/')
def get_all():
    entities = image_repo.get_all()
    images = [schemas.Image.from_orm(entity).dict() for entity in entities]
    return jsonify(images), HTTPStatus.OK


@view.delete('/<uid>')
def delete_image(uid):
    image_repo.delete(uid)
    return {}, HTTPStatus.NO_CONTENT


@view.put('/<uid>')
def update_route(uid):
    payload = request.json
    payload['uid'] = uid
    new_image = schemas.Image(**payload)

    entity = image_repo.update(**new_image.dict())

    new_image = schemas.Image.from_orm(entity)
    return new_image.dict(), HTTPStatus.OK
