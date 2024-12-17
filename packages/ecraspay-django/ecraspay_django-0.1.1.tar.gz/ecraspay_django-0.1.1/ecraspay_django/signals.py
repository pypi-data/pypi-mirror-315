from django.dispatch import receiver

from ecraspay_django.signals import webhook_received


@receiver(webhook_received)
def handle_webhook(sender, request, event, **kwargs):
    """
    Handle incoming webhook events from Ecraspay.

    Args:
        sender (Signal): The signal that triggered the receiver.
        request (Request): The incoming HTTP request.
        event (dict): The webhook event data.
    """
    print("Received webhook event:", event)
    print("Request data:", request.data)
