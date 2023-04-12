import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def forbidden_symbols(username):
    right_list = re.findall(r'[\w.@+-]+', username)
    bad_chars = username
    for item in right_list:
        bad_chars = bad_chars.replace(item, "")
    return bad_chars


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(f'Год {value} больше текущего!')


def validate_username(value):
    if value == 'me':
        raise ValidationError(f'{value} служебное имя!')
    if not re.fullmatch(r'[\w.@+-]+\Z', value):
        raise ValidationError(
            f'Имя пользователя {value} содержит запрещенные символы - '
            f'{forbidden_symbols(value)}. '
            'может содержать только буквы, цифры и знаки (@.+- _) .'
        )
