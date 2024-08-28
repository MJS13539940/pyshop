from decimal import Decimal
from django.shortcuts import render, redirect, reverse, get_object_or_404
# from django.urls import reverse
from django.conf import settings
import stripe

from orders.models import Order


# Create your views here.
#stripe 인스턴스 생성
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

#결제 프로세스
def payment_process(request):
    #주문을 위한 아이디
    order_id = request.session.get('order_id', None) #세션정보를 받아옴
    order = get_object_or_404(Order, id=order_id) #주문정보를 받아옴

    #리퀘스트를 확인함
    if request.method == 'POST':
        # 경로를 식별자(uri)로 인식해서 쓴다.
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        #stripe 결제 세션 데이터
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [] #주문항목이 들어올 자리
        }

        #주문항목 추가
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')), #센트 개념을 해결하기위한 방안중 하나
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },

                'quantity': item.quantity,
            })


        # stripe 결제 세션 생성
        session = stripe.checkout.Session.create(**session_data)

        # stripe 결제 양식으로 리디렉션
        return redirect(session.url, code=303)


    else:
        return render(request, 'payment/process.html', locals()) #로컬 화면으로 넘어감(결제 안됨)


#결제 성공
def payment_completed(request):
    return render(request, 'payment/completed.html')


#결제 취소
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

