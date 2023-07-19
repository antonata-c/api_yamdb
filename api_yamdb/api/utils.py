from datetime import datetime

from django.core.mail import send_mail


def send_letter(email, confirmation_code):
    """Отправка письма с кодом подтверждения."""

    send_mail(
        'Письмо с кодом подтверждения',
        f'Код подтверждения - {confirmation_code}',
        'donotreply@yamdb.ru',
        (email,),
        False,
    )


def get_current_year():
    return datetime.now().year
