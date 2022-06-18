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

    resp = s3.list_buckets()
    all_buckets = [bucket['Name'] for bucket in resp['Buckets']]

    for bucket in [
        config.aws.bucket_input_images,
        config.aws.bucket_output_images,
        config.aws.bucket_output_cvs
    ]:
        if bucket not in all_buckets:
            s3.create_bucket(Bucket=bucket)

    s3.upload_file(str(upload_path), config.aws.bucket_input_images, filename)

    os.remove(upload_path)

    http = urllib3.PoolManager()
    url = f'{config.server.endpoint}/api/v1/images/'
    payload = {'name': filename, 'path': f'{config.aws.bucket_input_images}/{filename}'}
    encoded_data = json.dumps(payload).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})

    return filename, HTTPStatus.OK
