from django.conf import settings
from django.core.mail import send_mail


def send_letter(email, confirmation_code):
    """Отправка письма с кодом подтверждения."""

    send_mail(
        'Письмо с кодом подтверждения',
        f'Код подтверждения - {confirmation_code}',
        settings.EMAIL_YAMDB_ADDRESS,
        (email,),
        False,
    )
