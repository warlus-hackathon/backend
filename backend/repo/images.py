from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import DataImage


class Image:
    name = 'image'

    def add_images(self, name: str, path: str) -> DataImage:
        try:
            new_image = DataImage(name=name, path=path)
            db_session.add(new_image)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return new_image

    def get_all(self) -> list[DataImage]:
        return DataImage.query.all()

    def get_by_id(self, uid: int) -> DataImage:
        image = DataImage.query.filter(DataImage.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)
        return image

    def get_not_recognized(self) -> DataImage:
        image = DataImage.query.filter(DataImage.obj_number == -1).first()
        if not image:
            raise NotFoundError(self.name)
        return image

    def delete(self, uid: int) -> None:
        image = DataImage.query.filter(DataImage.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)
        db_session.delete(image)
        db_session.commit()

    def update(self, name: str, uid: int, path: str, obj_number: int, was_recognized: int) -> DataImage:
        image = DataImage.query.filter(DataImage.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)

        try:
            image.name = name
            image.path = path
            image.obj_number = obj_number
            image.was_recognized = was_recognized
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return image
