from django.contrib import admin

from shop.models import Category, Product

# Register your models here.

# 어드민에 등록하는 데코레이터 레지스터
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #표시할 영역
    list_display = ['name', 'slug']
    #사전공개하는 필드
    prepopulated_fields = {'slug': ('name',)} #슬러그를 키로 쓴다

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    
