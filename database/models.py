import datetime

from peewee import IntegerField, CharField, DateTimeField

from .base import BaseModel, db


class Users(BaseModel):
    id = IntegerField(primary_key=True)
    token = CharField(null=True)
    user_id = IntegerField()
    first_name = CharField()
    username = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)


def init_db():
    db.connect()
    db.create_tables([Users])
