from config.celery import app
from django.core.mail import send_mail

@app.task
def send_purchase_email(owner_email, product_name, quantity, buyer_username):
    subject = f'Покупка товара: {product_name}'
    message = f'Продукт "{product_name}" был куплен в количестве {quantity} пользователем {buyer_username}.'
    from_email = 'fitstreety@gmail.com'
    recipient_list = [owner_email]

    send_mail(subject, message, from_email, recipient_list)
@app.task
def send_review_notification_email(product_owner_email, reviewer_username, product_title, review_content):
    subject = 'Новый комментарий к вашему товару'
    message = f'Пользователь {reviewer_username} оставил комментарий к вашему товару "{product_title}":\n\n{review_content}'
    from_email = 'fitstreety@gmail.com'
    recipient_list = [product_owner_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)