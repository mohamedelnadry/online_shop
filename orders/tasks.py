from celery import shared_task

from django.core.mail import send_mail

from .models import Order

@shared_task
def order_created(order_id):
    # taks to send email notify while creating order

    order = Order.objects.get(id=order_id)
    subject = f'order {order.id}'
    message = f'Dear {order.first_name},' f'You have successfully placed an order and your order id {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@shop.com',[order.email])

    return mail_sent

