import os

from pydantic import BaseModel


class Server(BaseModel):
    endpoint: str
    port: str
    host: str


class DataBase(BaseModel):
    url: str


class AwsConfig(BaseModel):
    endpoint: str
    key_id: str
    key: str
    bucket_input_images: str
    bucket_output_images: str
    bucket_output_cvs: str


class AppConfig(BaseModel):
    server: Server
    db: DataBase
    aws: AwsConfig


def load_from_env() -> AppConfig:
    app_endpoint = os.environ['APP_ENDPOINT']
    app_port = os.environ['APP_PORT']
    app_host = os.environ['APP_HOST']
    db_url = os.environ['DB_URL']
    aws_endpoint = os.environ['AWS_ENDPOINT']
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_bucket_input_images = os.environ['AWS_BUCKET_NAME_INPUT_IMAGES']
    aws_bucket_output_images = os.environ['AWS_BUCKET_NAME_OUTPUT_IMAGES']
    aws_bucket_output_cvs = os.environ['AWS_BUCKET_NAME_OUTPUT_CVS']
    return AppConfig(
        server=Server(endpoint=app_endpoint, port=app_port, host=app_host),
        db=DataBase(url=db_url),
        aws=AwsConfig(
            endpoint=aws_endpoint,
            key_id=aws_access_key_id,
            key=aws_secret_access_key,
            bucket_input_images=aws_bucket_input_images,
            bucket_output_images=aws_bucket_output_images,
            bucket_output_cvs=aws_bucket_output_cvs,
        )
    )


config = load_from_env()
