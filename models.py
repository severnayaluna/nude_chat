from peewee import *

db = SqliteDatabase('users.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -32*1000})


class User(Model):

    name = CharField(max_length=256, null=True)
    tgid = IntegerField()
    description = TextField(null=True)
    age = IntegerField(null=True)

    class Meta:
        database = db


class Room(Model):

    first_user_id = ForeignKeyField(User, on_delete='CASCADE', related_name='first_user_id')
    second_user_id = ForeignKeyField(User, on_delete='CASCADE', related_name='second_user_id')

    class Meta:
        database = db


db.create_tables([User, Room])