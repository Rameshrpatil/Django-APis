from django.db import models

class Transaction(models.Model):
    PAYMENT_CHOICES = (('razorpay', 'Razorpay'), ('stripe', 'Stripe'))
    
    payment_id = models.CharField(max_length=100, blank=True)
    order_id = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    payment_gateway = models.CharField(choices=PAYMENT_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_gateway} - {self.status} - {self.amount}"
