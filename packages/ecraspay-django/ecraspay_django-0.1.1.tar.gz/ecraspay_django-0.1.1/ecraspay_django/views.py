from django.dispatch import Signal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentInitiationSerializer


webhook_received = Signal(providing_args=["request", "event"])


class WebhookView(APIView):
    """
    A Django REST framework view to handle incoming webhook events from Ecraspay.

    This view receives webhook events from Ecraspay and triggers signals for further processing.

    Methods:
        post(request): Handle incoming webhook events from Ecraspay.
    """

    def post(self, request):
        """
        Handle incoming webhook events from Ecraspay.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: The HTTP response.
        """
        event = request.data
        webhook_received.send(sender=self.__class__, request=request, event=event)

        return Response(status=status.HTTP_200_OK)


class PaymentView(APIView):
    """
    A Django REST framework view to handle payment-related operations.

    This view provides endpoints to initiate and verify payments.

    Methods:
        post(request): Initiate a new payment transaction.
        get(request): Verify the status of a payment transaction.
    """

    def post(self, request):
        """
        Initiate a new payment transaction.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: The HTTP response.
        """
        pass


class PaymentVerificationView(APIView):
    """
    A Django REST framework view to handle payment verification operations.

    This view provides an endpoint to verify the status of a payment transaction.

    Methods:
        get(request): Verify the status of a payment transaction.
    """

    def get(self, request, payment_id):
        """
        Verify the status of a payment transaction.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: The HTTP response.
        """
        pass
