from peewee import SqliteDatabase, Model

db = SqliteDatabase('database/database.db')


class BaseModel(Model):
    class Meta:
        database = db
