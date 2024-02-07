from .send_email import send_confirmation_email, send_password_reset_email, is_vip_email
from celery import shared_task
from config.celery import app

# @shared_task
@app.task
def send_confirm_email_task(email, code):
    send_confirmation_email(email, code)


@app.task
def send_password_reset_task(email, user_id):
    send_password_reset_email(email, user_id)

@app.task
def send_vip_email_task(email, username):
    is_vip_email(email, username)
# shared_task | app.task