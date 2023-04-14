import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def forbidden_symbols(username):
    """Сформировать строку из недопустимых символов в username"""
    return ''.join(re.split(r'[\w.@+-]+', username))


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Произведения из будущего {value}г., в текущем '
            f'{timezone.now().year}г., к рассмотрению не принимаются!')
    return value


def validate_username(value):
    if value == 'me':
        raise ValidationError(f'{value} служебное имя!')
    else:
        bad_symbols = forbidden_symbols(value)
        if bad_symbols != '':
            raise ValidationError(
                f'Имя пользователя {value} содержит'
                f' запрещенные символы - {bad_symbols},'
                f'а должно начинаться с буквы и содержать'
                ' внутри только буквы, цифры и знаки (@.+-_).'
            )
