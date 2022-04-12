from django.urls import path, re_path
from .views import *
from .mobileOtp import *
from .sellerView import *





urlpatterns = [
    path('register',RegisterView.as_view(), name='register'),
    path('login', loginView, name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('sendOtp', send_otp, name='sendOtp'),
    path('verifyOtp', verfiy_otp, name='verfityOtp'),
    path('cart',CartView.as_view(), name='carts'),
    path('address', AddressView.as_view(), name='addres'),
    path('order', OrderView.as_view(), name='orders'),
    path('category', CategoryView.as_view(), name='categorys'),
    path('product',ProductView.as_view(), name='products'),
    path('notification',NotificationView.as_view(), name='notifications'),

    
#   ! SELLLER SIDE URLS
    
    path('selproduct',SelProductView.as_view(), name='selprod'),
    path('selorder',SelOrderView.as_view(), name='selorder'),

 
]