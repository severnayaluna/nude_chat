from peewee import *
from exceptions import *
from services.validator import *


db = SqliteDatabase(
    'users.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})


class User(Model):
    name = CharField(max_length=256, null=True)
    tgid = IntegerField(unique=True)
    description = TextField(null=True)
    age = IntegerField(null=True)
    # reg = BooleanField(default=False)

    def set_name(self, name):
        try:
            validate_name(name)
            self.name = name
            self.save()
            return False
        except BadName as ex:
            return f'{ex}'
        
    def set_age(self, age):
        try:
            validate_age(age)
            self.age = age
            self.save()
            return False
        except BadAge as ex:
            return f'{ex}'
    
    def set_description(self, text):
        self.description = text
        self.save()


    class Meta:
        database = db


class Room(Model):
    first_user_id = ForeignKeyField(
        User,
        on_delete='CASCADE',
        related_name='first_user_id')
    second_user_id = ForeignKeyField(
        User,
        on_delete='CASCADE',
        related_name='second_user_id')

    class Meta:
        database = db


db.create_tables([User, Room])