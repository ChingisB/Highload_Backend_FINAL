from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, Payment

app = Celery('final')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Order Confirmation - {order.id}"
    message = f"Thank you for your order, {order.user.username}. Your order total is {order.total_amount}."
    recipient_list = [order.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@app.task
def process_payment(payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.status = 'PROCESSED'
    payment.save()
