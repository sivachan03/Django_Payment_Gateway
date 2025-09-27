from django.shortcuts import render
from .models import *
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import razorpay


client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

# Create your views here.
class ProductListView(View):
    def get(self,request):
        product=Product.objects.all()
        return render(request,"product/product.html",{"product_list":product})
    
class CheckoutView(LoginRequiredMixin,View):
    def get(self,request,product_id):
        produt=get_object_or_404(Product,id=product_id)
        return render(request,"product/checkout.html",{"pro":produt})
@method_decorator(csrf_exempt,name="dispatch")

    
class CreatePaymentView(LoginRequiredMixin,View):
    def post(self,request,product_id):
        product=get_object_or_404(Product,id=product_id)
        order_data={
            "amount":int(product.price),
            "currency":"INR",
            "payment_capture":'1'
                    }
        razorpay_order=client.order.create(order_data)
        Order.objects.create(
            user=request.user,
            product=product,
            amount=product.price,
            razorpay_order_id=razorpay_order["id"]

        )
        return JsonResponse({
            "order_id":razorpay_order["id"],
            "razorpay_key_id":settings.RAZORPAY_KEY_ID,
            "product_name":product.name,
            "amount":order_data["amount"],
            "razorpay_callback_url":settings.RAZORPAY_CALLBACK_URL
        })
            
@method_decorator(csrf_exempt, name="dispatch")
class PaymentCallbackView(View):
   
    def post(self,request):
        if "razorpay_signature" in request.POST:
            order_id=request.POST.get("razorpay_order_id")
            payment_id=request.POST.get("razorpay_payment_id")
            signature=request.POST.get("razorpay_signature")
            order=get_object_or_404(Order,razorpay_order_id=order_id)
            if client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
  }):
                order.razorpay_payment_id=payment_id
                order.razorpay_signature=signature
                order.is_paid=True
                order.save()
                return render(request, "product/payment_success.html", {"order": order})

            else:
                order.is_paid=False
                order.save()
                return JsonResponse({"status": "failed"})
        else:
            return JsonResponse({"status": "failed"})

class PaymentSuccessView(View):
    def get(self, request):
        return render(request, "product/payment_success.html")

class PaymentFailedView(View):
    def get(self, request):
        return render(request, "product/payment_failed.html")
