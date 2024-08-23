from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'), #아무 경로 없을때 리스트를 바로 보여줌
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

