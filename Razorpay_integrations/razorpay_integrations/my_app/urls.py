from django.urls import path
from . import views

urlpatterns = [
    path('razorpay/', views.razorpay_payment, name='razorpay_payment'),
    path('stripe/', views.stripe_payment, name='stripe_payment'),
    path('success/', views.success, name='success'),
]
