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
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'в username используются недопустимые '
            'символы: {bad_symbol}'.format(
                bad_symbol=''.join(re.split(r'[\w.@+-]+', value))
            )
        )
    return value
