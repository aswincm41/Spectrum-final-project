from django.contrib import admin
from.models import Categories,Brand,Filter_price,Product,Contact,OrderItem,Order
# Register your models here.
admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Filter_price)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderItem)