from django.core.mail import send_mail
from django.utils.html import format_html
from django.core.mail import EmailMultiAlternatives
from decouple import config

URL = config('URL')

def send_confirmation_email(email, code):
    activation_url = code
    html_message = format_html(
        'Здравствуйте, активируйте ваш аккаунт'
        '<br>'
        'Чтобы активировать аккаунт, введите этот код в приложении: '
        '<br>'
        '<h3>{}</h3>'
        '<br>'
        'Не передавайте код никому',
        activation_url
    )

    msg = EmailMultiAlternatives(
        'Здравствуйте',
        'Активируйте ваш аккаунт',
        'test@gmail.com',
        [email]
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()
   

def send_password_reset_email(email, user_id):
    password_reset_url = f'{URL}/account/password_change/{user_id}/'
    message = format_html(
        'Здравствуйте, чтобы восстановить пароль, перейдите по ссылке:'
        '<br>'
        '<a href="{0}">{0}</a>'
        '<br>'
        'Не передавайте данную ссылку никому.',
        password_reset_url
    )

    send_mail(
        'Восстановление пароля',
        '',
        'test@gmail.com',
        [email],
        fail_silently=False,
        html_message=message
    )
def is_vip_email(email, username):
    message = format_html(
        "Поздравляю {},  вы стали вип пользователем",
        username
    )
    send_mail(
        'Здравствуйте',
        message,
        'test@gmail.com',
        [email],
        fail_silently=False
    )