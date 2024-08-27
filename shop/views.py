from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category) #카테고리에 해당하는 물품만 들고오게된다.

    return render(request, 'shop/product/list.html', 
                  {'category': category, 'categories': categories, 'products': products})



def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # 카트에 제품 추가
    cart_product_form = CartAddProductForm()

    return render(request, 'shop/product/detail.html', 
                  {'product': product,
                   'cart_product_form': cart_product_form})
