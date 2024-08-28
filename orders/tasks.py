#주문 접수 시 사용자에게 확인 이메일 보내기

from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task #태스크를 공유하도록 설정
def order_created(order_id): #주문이 생성됐을때 동작하도록하기
    order = Order.objects.get(id=order_id)
    subject = f'Order no. {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@pyshop.com', [order.email])

    return mail_sent
