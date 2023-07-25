import datetime
import re

from django.core.exceptions import ValidationError

NAME_TEMPLATE = r'[\w.@+-]'


def username_validator(username):
    # Тут хотел спросить зачем так было нужно? сократить строку?
    username_symbols = ''.join(set(username))
    subbed = re.sub(NAME_TEMPLATE, '', username_symbols)
    if username == 'me':
        raise ValidationError('Использовать имя "me" запрещено!')
    if subbed:
        raise ValidationError(
            f'Использованы запрещенные символы: {subbed}'
        )
    return username


def get_current_year():
    return datetime.datetime.now().year
