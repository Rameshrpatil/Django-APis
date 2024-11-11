import razorpay
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction

# Initialize Stripe
stripe.api_key = settings.STRIPE_API_KEY

# Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

def home(request):
    return render(request, 'payments/home.html')

# Razorpay Payment View
def razorpay_payment(request):
    if request.method == "POST":
        amount = 50000  # Amount in paise (500 INR)
        currency = 'INR'

        # Create Razorpay Order
        razorpay_order = razorpay_client.order.create({
            'amount': amount,
            'currency': currency,
            'payment_capture': '1'
        })

        # Create Transaction Record
        transaction = Transaction.objects.create(
            payment_id=razorpay_order['id'],
            amount=amount / 100,
            currency=currency,
            status='Pending',
            payment_gateway='razorpay'
        )

        context = {
            'order': razorpay_order,
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'transaction_id': transaction.id
        }
        return render(request, 'payments/razorpay_payment.html', context)

    return render(request, 'payments/home.html')

# Razorpay Success Callback
@csrf_exempt
def razorpay_success(request):
    if request.method == "POST":
        # You can verify the payment signature here for security
        transaction_id = request.POST.get('transaction_id')
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.status = 'Success'
        transaction.save()
        return redirect('success')
    return redirect('home')

# Stripe Payment View
def stripe_payment(request):
    if request.method == "POST":
        amount = 5000  # Amount in cents (50 USD)
        currency = 'usd'

        # Create Stripe Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card'],
        )

        # Create Transaction Record
        transaction = Transaction.objects.create(
            payment_id=intent.id,
            amount=amount / 100,
            currency=currency,
            status='Pending',
            payment_gateway='stripe'
        )

        context = {
            'client_secret': intent.client_secret,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'transaction_id': transaction.id
        }
        return render(request, 'payments/stripe_payment.html', context)

    return render(request, 'payments/home.html')

# Stripe Success Callback
@csrf_exempt
def stripe_success(request):
    if request.method == "POST":
        # You should verify the Stripe signature here for security
        transaction_id = request.POST.get('transaction_id')
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.status = 'Success'
        transaction.save()
        return redirect('success')
    return redirect('home')

# Success Page
def success(request):
    return render(request, 'payments/success.html')
