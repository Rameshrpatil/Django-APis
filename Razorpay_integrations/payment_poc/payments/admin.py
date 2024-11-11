from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_gateway', 'amount', 'status', 'created_at')
    list_filter = ('payment_gateway', 'status')
    search_fields = ('payment_id', 'order_id')
