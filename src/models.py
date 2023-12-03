from peewee import CharField, IntegerField, TextField, Model

import settings


class User(Model):
    """
    Класс юзера в бд.
    """
    name = CharField(max_length=256, null=True) # имя юзера
    tgid = IntegerField(unique=True) # телеграм айди юзера
    description = TextField(null=True) # БИО юзера
    age = IntegerField(null=True) # возраст юзера

    class Meta:
        database = settings.MAIN_DB
