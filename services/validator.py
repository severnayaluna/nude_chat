from exceptions import *

def validate_name(name):
    if len(name) < 2 or len(name) > 256:
        raise BadName('Длина имени должна быть от 2 до 256 символов!')


def validate_age(age):
    try:
        age = int(age)
    except ValueError:
        raise BadAge('Возраст должен быть целым положительным числом!')
    if not(0 <= age < 121):
        raise BadAge('Возраст должен быть от 0 до 120!')