from django.urls import reverse
from django.shortcuts import render, redirect

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from orders.tasks import order_created

# Create your views here.
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            #전부 주문했으므로 카트는 비우기
            cart.clear()

            #비동기 작업을 실행
            order_created.delay(order.id) #order.id에 대해서 order_created를 잠깐 대기시킨다.

            #세션 순서 결정
            request.session['order_id'] = order.id
            #결제 리디렉션
            return redirect(reverse('payment:process'))

            # return render(request, 'orders/order/created.html', {'order': order})

    else:
        form = OrderCreateForm()

    #form이 valid 할때와 아닐때의 들고가는 정보가 다른 채로 렌더링된다.(?)
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


# request.method에 따른 작업 내용

# GET 요청
# OrderCreateForm 폼을 인스턴스화
# orders/order/create.html 템플릿을 렌더링
# POST 요청
# 전송된 데이터의 유효성 검사
# 데이터가 유효하면 order = form.save()를 사용하여 데이터베이스에 새로운 주문을 생성
# 카트의 아이템들을 반복해서 각 아이템에 대한 OrderItem을 생성
# 카트의 콘텐츠 삭제
# orders/order/created.html 템플릿을 렌더링