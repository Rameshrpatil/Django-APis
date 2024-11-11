from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('razorpay/', views.razorpay_payment, name='razorpay_payment'),
    path('razorpay/success/', views.razorpay_success, name='razorpay_success'),
    path('stripe/', views.stripe_payment, name='stripe_payment'),
    path('stripe/success/', views.stripe_success, name='stripe_success'),
    path('success/', views.success, name='success'),
]
