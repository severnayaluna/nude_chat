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
        """
        Стэйт
        """        
        name: str = 'name' # стэйт ожидания имя юзера
        age: str = 'age' # стэйт ожидания возраста юзера
        description: str = 'description' # стэйт ожидания БИО юзера
        ended: str = 'ended' # стэйт законченной регистрации


    name = CharField(max_length=256, null=True) # имя юзера
    tgid = IntegerField(unique=True) # телеграм айди юзера
    description = TextField(null=True) # БИО юзера
    age = IntegerField(null=True) # возраст юзера
    reg = BooleanField(default=False) # зарегистрирован ли юзер
    state = TextField(choices=State.choices, null=True) # стэйт юзера


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
