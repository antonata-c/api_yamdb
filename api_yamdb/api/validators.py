from django.core.exceptions import ValidationError


def username_validator(username):
    if username == "me":
        raise ValidationError('Имя пользователя "me" использовать нельзя!')
    return username
