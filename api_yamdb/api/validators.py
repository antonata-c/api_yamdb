import re

from django.core.exceptions import ValidationError


def username_validator(username):
    subbed = re.sub(r'[\w.@+-]', '', username)
    if username == 'me':
        raise ValidationError('Использовать имя "me" запрещено!')
    elif subbed:
        raise ValidationError(
            f'Использованы запрещенные символы: {subbed}'
        )
    return username
