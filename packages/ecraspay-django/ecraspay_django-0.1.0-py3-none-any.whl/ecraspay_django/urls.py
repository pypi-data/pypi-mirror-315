from django.urls import path

from ecraspay_django.views import PaymentView, PaymentVerificationView

urlpatterns = [
    path("payment/", PaymentView.as_view(), name="payment"),
    path(
        "payment/verify/<str:payment_id>/",
        PaymentVerificationView.as_view(),
        name="payment-verification",
    ),
]
