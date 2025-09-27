
from django.urls import path
from Product import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.ProductListView.as_view(),name='product_list'),
    path('checkout/<int:product_id>/', views.CheckoutView.as_view() , name='checkout'),
    path('create_payment/<int:product_id>/',views.CreatePaymentView.as_view(),name="create_payment"),
    
    path("payment-verify/", views.PaymentCallbackView.as_view(), name="payment_callback"),
    path("payment-success/",views. PaymentSuccessView.as_view(), name="payment_success"),
    path("payment-failed/", views.PaymentFailedView.as_view(), name="payment_failed"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
