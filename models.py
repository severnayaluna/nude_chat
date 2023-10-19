from peewee import *

from services.exceptions import *
from services.validator import *
from services.custom_state.base_state import BaseState, State

from typing import Union


db = SqliteDatabase(
    'users.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})


class User(Model):
    class RegState(BaseState):
        """
        Регистрационный стэйт
        """        
        name: State = State('name') # стэйт ожидания имя юзера
        age: State = State('age') # стэйт ожидания возраста юзера
        description: State = State('description') # стэйт ожидания БИО юзера
        ended: State = State('ended') # стэйт законченной регистрации
    
    class FindState(BaseState):
        in_find: State = State('in_find')
        not_in_find: State = State('not_in_find')


    name = CharField(max_length=256, null=True) # имя юзера
    tgid = IntegerField(unique=True) # телеграм айди юзера
    description = TextField(null=True) # БИО юзера
    age = IntegerField(null=True) # возраст юзера
    reg_state = TextField(null=True) # стэйт юзера
    find_state = TextField(null=True) # стэйт юзера


    @classmethod
    def get_or_create_by_msg(cls, message):
        """Функция, которая создает и возвращает юзера по сообщению.

        Args:
            message (types.Message): сообщение от юзера

        Returns:
            tuple[User, bool]: кортеж (юзер, существовал-ли-до)
        """        
        return tuple(cls.get_or_create(tgid=message.from_user.id))

    @classmethod
    def get_by_msg(cls, message):
        """Функция, которая возвращает юзера по сообщению.

        Args:
            message (types.Message): сообщение от юзера

        Returns:
            User: юзер
        """          
        return cls.get(tgid=message.from_user.id)

    def get_state(self, name: str):
        return State(getattr(self, name))

    def set_state(self, name: str, state: State):
        setattr(self, name, state.state)
        self.save()

    def set_state(self, name: str, state: State):
        setattr(self, name, state.state)
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
