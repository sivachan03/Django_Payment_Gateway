from django.db import models
from django.contrib.auth.models import User
from .models import *
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    images=models.ImageField(blank=True, null=True,upload_to="Products/")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveBigIntegerField()

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)  # fixed lowercase p
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # fixed naming

    def __str__(self):
        return f"Order {self.id}"
    
# models.py
from django.db import models

class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='slider/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title or "Slider Image"
