from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/',views.product, name='product'),
    path('search/',views.search, name='search'),
    path('<str:id>',views.singleproduct,name='singleproduct'),
    path('contact/',views.contact,name='contact'),
    path('about/', views.about_page, name='about'),
    path('registration/',views.registration,name='registration'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),


    # path('cart_detalis/',views.cart_detalis,name='cart_detalis'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('reciept/',views.reciept,name='reciept'),
]

