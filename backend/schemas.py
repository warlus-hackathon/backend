from typing import Optional

from pydantic import BaseModel


class Schema(BaseModel):

    class Config:
        orm_mode = True


class Image(Schema):
    uid: int
    name: str
    path: str
    obj_number: Optional[int]
    was_recognized: Optional[int]
