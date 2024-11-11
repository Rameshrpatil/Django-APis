import razorpay
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Transaction

# Configure Stripe
stripe.api_key = settings.STRIPE_API_KEY

def razorpay_payment(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    amount = 50000  # Amount in paise (500 INR)

    payment_order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    transaction = Transaction.objects.create(
        payment_id=payment_order['id'],
        amount=amount / 100,
        status='Pending',
        payment_gateway='razorpay'
    )

    return render(request, 'my_app/razorpay_payment.html', {
        'order': payment_order,
        'razorpay_key': settings.RAZORPAY_API_KEY,
        'transaction_id': transaction.id
    })

def stripe_payment(request):
    amount = 5000  # Amount in cents (50 USD)

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        payment_method_types=['card']
    )

    transaction = Transaction.objects.create(
        payment_id=intent.id,
        amount=amount / 100,
        status='Pending',
        payment_gateway='stripe'
    )

    return render(request, 'my_app/stripe_payment.html', {
        'client_secret': intent.client_secret,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'transaction_id': transaction.id
    })

def success(request):
    return render(request, 'my_app/success.html')
