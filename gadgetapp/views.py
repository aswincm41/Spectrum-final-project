from django.shortcuts import render,redirect
from django.http import HttpResponse
from.models import Product,Categories,Filter_price,Brand,Contact,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
import razorpay
from django.conf import settings

client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

def index(request):
    product = Product.objects.filter(status = 'PUBLISHED')
    context = {'product':product,}
    return render(request, 'index.html',context)

def product(request):
    product = Product.objects.filter(status = 'PUBLISHED')
    Category = Categories.objects.all()
    price = Filter_price.objects.all()
    brand = Brand.objects.all()
    CATID= request.GET.get('category')
    priceid = request.GET.get('filter_price')
    brandid = request.GET.get('brand')
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    LOWTOHIGH =request.GET.get('LOWTOHIGH')
    HIGHTOLOW =request.GET.get('HIGHTOLOW')
    NEWID = request.GET.get('NEW')
    OLDID = request.GET.get('OLD')
    if CATID:
        product = Product.objects.filter(category=CATID)
    elif priceid:
        product=Product.objects.filter(filter_price=priceid)
    
    elif brandid:
        product=Product.objects.filter(brand=brandid)
    elif ATOZID:
        product=Product.objects.filter(status = 'PUBLISHED').order_by('name')
    elif ZTOAID:
        product=Product.objects.filter(status = 'PUBLISHED').order_by('-name')
    elif LOWTOHIGH:
        product=Product.objects.filter(status = 'PUBLISHED').order_by('price')
    elif HIGHTOLOW:
        product=Product.objects.filter(status = 'PUBLISHED').order_by('-price')
    elif NEWID:
        product=Product.objects.filter(status = 'PUBLISHED', Condition = 'NEW').order_by('-id')
    elif OLDID:
        product=Product.objects.filter(status = 'PUBLISHED', Condition = 'OLD').order_by('-id')
    
    else:
        product = Product.objects.filter(status ='PUBLISHED')
       


    context = {'product':product, 'Category':Category, 'price':price, 'brand':brand}
    return render(request, 'product.html',context)






def search(request):
    query = request.GET.get('query')
    product=Product.objects.filter(name__icontains=query)
    context={'product':product}
    return render(request, 'search.html',context)
def singleproduct(request,id):
    prod=Product.objects.filter(id=id).first()
    context={'prod':prod}
    return render(request, 'singleproduct.html',context)

def about_page(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email= request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
        return redirect('index')
    return render(request,'contact.html')

def registration(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')

        a = User.objects.create_user(username,email,pass1)
        a.first_name=first_name
        a.last_name=last_name
        a.save()
        

        return redirect('login')
    return render(request,'registration.html') 

def login(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('index')
        else:
            return redirect('login')
    return render(request,'login.html')



from django.contrib.auth import logout as auth_logout
def logout(request):
    auth_logout(request)
    return redirect('/')




def placeorder(request):
    if request.method == 'POST': 
        cart=request.session.get('cart')
        UID=request.session.get('_auth_user_id')
        user=User.obejcts.get(id=UID)
        firstname= request.POST.get('firstname')
        lastname= request.POST.get('lastname')
        country= request.POST.get('country')
        address= request.POST.get('address')
        city= request.POST.get('city')
        state= request.POST.get('state')
        postcode= request.POST.get('postcode')
        phonenumber= request.POST.get('phonenumber')
        email= request.POST.get('email')
        amount= request.POST.get('amount')
        payment= request.POST.get('payment')
        order_id=request.POST.get('order_id')
        order=Order(user=user,firstname=firstname,lastname=lastname,country=country,address=address,city=city,state=state,postcode=postcode,phonenumber=phonenumber,email=email,payment=payment,amount=amount,payment_id=order_id)
        order.save()
        for i in cart:
            c=cart[i]['price']
            d=cart[i]['quantity']
            total=c*d
            item=OrderItem(order=order,product=cart[i]['name'],image=cart[i]['image'],quantity=cart[i]['quantity'],price=cart[i]['price'],total=total)
            item.save()
    return render(request,'placeorder.html')



##cart details

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'cart_details.html')

def checkout(request):
    payment=client.order.create({'amount':500,'currency':'INR','payment_capture':'1'})
    order_id=payment['id']
    context={'order_id':order_id,'payment':payment}
    return render(request,'checkout.html',context)

def wishlist(request):
    return render(request,'wishlist.html')


def reciept(request):
    totalAmount = calculateTotalAmount(request)  # Pass the request object to the function
    response = get_payment_response()  # Implement this function to get the Razorpay payment response

    context = {
        'totalAmount': totalAmount,
        'response': response,
    }

    return render(request, 'reciept.html', context)


def calculateTotalAmount(request):
    # Ensure that the quantities and prices are converted to integers before performing calculations
    totalAmount = 0
    for key, value in request.session.get('cart', {}).items():
        totalAmount += int(value['price']) * int(value['quantity'])
    return totalAmount

def get_payment_response():
    # Implement your logic to get the Razorpay payment response
    # This can include fetching data from the payment gateway or any other source
    # For demonstration purposes, a dummy response is returned
    return {
        'razorpay_payment_id': 'rzp_test_bdhXja6YIYa195',
        'razorpay_order_id': '5Saohy8E0RUb5WqdVpE7iUEc',
        
    }