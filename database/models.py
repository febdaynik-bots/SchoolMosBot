import datetime

from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField
from playhouse.sqlite_ext import JSONField

from .base import BaseModel, db


class Users(BaseModel):
    id = IntegerField(primary_key=True)
    token = CharField(null=True)
    student_id = IntegerField(null=True)
    user_id = IntegerField()
    first_name = CharField()
    username = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)


class Notify(BaseModel):
    id = IntegerField(primary_key=True)
    user = ForeignKeyField(Users, backref='notify', field='user_id')
    marks = JSONField(default=[])
    homeworks = JSONField(default=[])
    date_marks = CharField(default='')
    date_homeworks = CharField(default='')
    # date = DateTimeField(default=datetime.datetime.now)


def init_db():
    db.connect()
    db.create_tables([Users, Notify])
