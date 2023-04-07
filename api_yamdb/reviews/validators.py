from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.utils.translation import gettext_lazy


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )

def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            gettext_lazy(f'{value} служебное имя!')
        )
    if not re.match(r'[\w.@+-]+\Z', value):
        raise ValidationError(gettext_lazy(f'{value} содержит запрещенные символы!'))