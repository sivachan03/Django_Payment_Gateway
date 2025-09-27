from django.contrib import admin
from .models import *
# Register your models

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name',"price","stock")
    search_fields=('name',)
    list_filter=("price",)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    search_fields=("user__username","product__name","razorpay_order_id")

    list_display = ("id", "user", "product", "amount", "is_paid", "created_at")
    readonly_fields = ("razorpay_order_id", "razorpay_payment_id", "razorpay_signature")
