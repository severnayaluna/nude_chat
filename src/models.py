from peewee import *


db = SqliteDatabase(
    'users.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})


class User(Model):
    name = CharField(max_length=256, null=True) # имя юзера
    tgid = IntegerField(unique=True) # телеграм айди юзера
    description = TextField(null=True) # БИО юзера
    age = IntegerField(null=True) # возраст юзера

    class Meta:
        database = db


db.create_tables([User,])
