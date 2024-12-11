# Asynchronous Processing with Celery

## Overview

This document explains how to set up asynchronous tasks for tasks such as sending order confirmation emails and processing payments using Celery.

## Prerequisites

1. **Setup Redis with Docker-Compose**:
   ```docker-compose
   redis:
    image: redis:alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
   ```
2. **Install celery**
    ```bash
    pip install celery
    pip install django-celery-beat
    ```

## Setup work settings
```python
CELERY_BROKER_URL = os.environ.get("REDIS_TASKS_URL")
CELERY_BEAT_SCHEDULE = {
    'send-order-confirmation-emails': {
        'task': 'myapp.tasks.send_order_confirmation_email',
        'schedule': 60.0,
    },
    'process-payments': {
        'task': 'myapp.tasks.process_payment',
        'schedule': 300.0,
    },
}
```

## Create tasks
```python
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
```

## Example usage
```python
def create_order(request):
    new_order = Order.objects.create(user=request.user, total_amount=100.0)
    

    send_order_confirmation_email.delay(new_order.id)
    process_payment.delay(new_order.id)
    
    return JsonResponse({'message': 'Order created and tasks are being processed.'})
```