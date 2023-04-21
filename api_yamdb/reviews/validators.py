import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def model_validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Произведения из будущего {value}г., в текущем '
            f'{timezone.now().year}г., к рассмотрению не принимаются!')
    return value


def model_validate_username(value):
    if value == 'me':
        raise ValidationError(f'{value} служебное имя!')
    bad_symbol = ''.join(set(''.join(re.sub(r'[\w.@+-]+', '', value))))
    if bad_symbol != '':
        raise ValidationError(
            f'в username используются недопустимые '
            f'символы: {bad_symbol}'
        )
    return value
