from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Filter_price(models.Model):
    Filter_price = (
        ('1000 To 10000', '100 To 2000'),
        ('2000 To 20000', '200 To 3000'),
        ('3000 To 30000', '300 To 4000'),
        ('4000 To 40000', '400 To 5000'),
    )
    price = models.CharField(choices=Filter_price,max_length=200)
    def __str__(self):
        return self.price
    

class Product(models.Model):
    CONDITION = (('NEW','NEW'),('OLD','OLD'))

    STOCK = (('INSTOCK','INSTOCK'),('OUTOFSTOCK','OUTOFSTOCK'))
    STATUS = (('PUBLISHED','PUBLISHED'),('COMINGSOON','COMINGSOON'))
    UNIQUE_ID = models.CharField(unique=True,max_length=100, null = False)
    image = models.ImageField(upload_to='Gadgethub')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    Condition = models.CharField(choices= CONDITION,max_length=200)
    description = models.TextField()
    stock = models.CharField(choices= STOCK,max_length=200)
    status = models.CharField(choices = STATUS,max_length=200)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_price,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

   
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    subject=models.CharField(max_length=200)
    message=models.TextField(max_length=200)
    def __str__(self) :
        return self.name

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=200)
    postcode=models.IntegerField()
    phonenumber=models.IntegerField()
    email=models.EmailField()
    amount=models.CharField(max_length=200)
    payment_id=models.CharField(max_length=200,null=True,blank=True)
    paid=models.BooleanField(default=False,null=True)
    def __str__(self) :
        return self.user

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.CharField(max_length=200)
    image=models.ImageField(upload_to='pictures')
    quantity=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    total=models.CharField(max_length=200)
    def __str__(self) :
        return self.order
    
