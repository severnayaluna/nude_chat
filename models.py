from peewee import *
from services.exceptions import *
from services.validator import *
from services.custom_state.base_state import BaseState


db = SqliteDatabase(
    'users.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})


class User(Model):
    class State(BaseState):
        name: str = 'name'
        age: str = 'age'
        description: str = 'description'
        ended: str = 'ended'


    name = CharField(max_length=256, null=True)
    tgid = IntegerField(unique=True)
    description = TextField(null=True)
    age = IntegerField(null=True)
    reg = BooleanField(default=False)
    state = TextField(choices=State.choices, null=True)


    @classmethod
    def get_or_create_by_msg(cls, message):
        return tuple(cls.get_or_create(tgid=message.from_user.id))

    @classmethod
    def get_by_msg(cls, message):
        return cls.get(tgid=message.from_user.id)

    def set_state(self, state: State):
        self.state = state
        self.save()

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
    
    def set_reg(self, reg: bool):
        self.reg = reg
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