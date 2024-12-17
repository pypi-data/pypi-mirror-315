from django.conf import settings
import os

# Define the version of your package
__version__ = "0.1.0"

# Define the default app configuration
default_app_config = "ecraspay_django.apps.EcraspayDjangoConfig"

# Define the default settings for the ecraspay_django package
ECRASPAY_DJANGO_SETTINGS = {
    "ECRASPAY_API_KEY": os.getenv("ECRASPAY_API_KEY", ""),
    "ECRASPAY_ENVIRONMENT": os.getenv("ECRASPAY_ENVIRONMENT", "sandbox"),
    "ECRASPAY_PAYMENT_MODEL": "ecraspay_django.Payment",
    "ECRASPAY_WEBHOOK_URL": os.getenv("ECRASPAY_WEBHOOK_URL", ""),
    "ECRAS_REDIRECT_URL": os.getenv("ECRAS_REDIRECT_URL", ""),
    "PAYMENT_PROCESSING_MODE": os.getenv("PAYMENT_PROCESSING_MODE", "checkout"),
    # "ECRASPAY_PAYMENT_METHOD_MODEL": "ecraspay_django.PaymentMethod",
    # "ECRASPAY_PAYMENT_METHOD_TYPE_MODEL": "ecraspay_django.PaymentMethodType",
    # "ECRASPAY_TRANSACTION_MODEL": "ecraspay_django.Transaction
}


def get_ecraspay_setting(name):
    """
    Get the value of an ecraspay_django setting.
    """
    return getattr(settings, name, ECRASPAY_DJANGO_SETTINGS[name])
