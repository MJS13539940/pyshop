from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    #메타데이터
    class Meta:
        #이름을 통해 정렬한다
        ordering = ['name']
        #필드 중 name 을 인덱스로 쓴다.
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # 위의 name을 문자열로 출력할 필요가 있을 때
    def __str__(self):
        return self.name
    
    #절대경로: 파일을 저장, 삭제, 업데이트 할 때 등에 필요함
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
                    #주소에 appname shop 속의 product_list_by_category 로 reverse
    


class Product(models.Model):
    # 제품이 자기의 카테고리 정보를 갖고있어야함.
    # 외부키로 쓰고 class Category 를 참고한다.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) #카테고리 A(1,2,3,4) 일 때 2를 삭제하면 A가 삭제되고, 그에따라 1,3,4도 같이 삭제될 수 있기 때문에 이부분에 대해선 따로 주의가 필요함.
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200) # 상품이름이 중복되더라도 구분하기 위함 + url등에 넣을 때 용이하게 할 수 있음
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) #models.IntegerField 등을 쓸때의 계산상의 오차를 방지하기 위함.
    available = models.BooleanField(default=True) #제품판매가 가능한지 아닌지 여부
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']), #id와 slug를 같이 인덱스로 쓴다.
            models.Index(fields=['name']),
            models.Index(fields=['-created']), # 정렬할 경우 내림차순으로 하기 위해 - 를 붙임
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    

