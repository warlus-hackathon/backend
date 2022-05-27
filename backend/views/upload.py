import json
import os
from http import HTTPStatus
from pathlib import Path

import urllib3
from flask import Blueprint, abort, request
from werkzeug.utils import secure_filename

from backend.aws import s3
from backend.config import config

view = Blueprint('upload', __name__)

upload_dir = Path('tmp')
upload_dir.mkdir(exist_ok=True, parents=True)


@view.post('/')
def download_file():

    if 'file' not in request.files:
        abort(HTTPStatus.BAD_REQUEST, 'В теле запроса должен передаваться файл ("file")')
    file = request.files['file']
    if not file.filename:
        abort(HTTPStatus.BAD_REQUEST, 'В теле запроса должен передаваться файл ("file")')
    filename = secure_filename(file.filename)
    if not (Path(filename).suffix in ('.jpg', '.jpeg', '.png', '.pdf')):
        abort(HTTPStatus.BAD_REQUEST, 'Неподдерживаемый формат файла')

    upload_path = upload_dir / filename

    file.save(upload_path)

    s3.upload_file(str(upload_path), config.aws.bucket_input_images, filename)

    os.remove(upload_path)

    http = urllib3.PoolManager()
    url = 'http://127.0.0.1:5001/api/v1/images/'
    payload = {'name': filename, 'path': f'{config.aws.bucket_input_images}/{filename}'}
    encoded_data = json.dumps(payload).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})

    return filename, HTTPStatus.OK
