from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ('receipt',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ('total_price',)
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_date')
    search_fields = ('order__id',)
    readonly_fields = ('order', 'amount', 'payment_date', 'receipt')
