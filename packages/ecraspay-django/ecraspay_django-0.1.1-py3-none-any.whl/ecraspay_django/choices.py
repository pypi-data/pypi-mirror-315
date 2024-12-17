from django.db import models


class PaymentStatusChoices(models.TextChoices):
    """
    Enum-like class representing the various statuses of a process, such as a payment.

    Attributes:
        PENDING (str): Payment has been initiated but not yet started.
        IN_PROGRESS (str): Payment process has started and is underway.
        SUCCESS (str): Payment process completed successfully.
        FAILED (str): Payment process encountered an error and did not complete.
        CANCELLED (str): Payment process was deliberately stopped before completion.
    """

    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class CurrencyChoices(models.TextChoices):
    """
    Enum-like class for representing currency choices in a Django model.

    Attributes:
        USD (str): United States Dollar.
        EUR (str): Euro, the official currency of the Eurozone.
        GBP (str): British Pound Sterling.
        NGN (str): Nigerian Naira, the official currency of Nigeria.
    """

    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    GBP = "GBP", "British Pound"
    NGN = "NGN", "Nigerian Naira"


class PaymentMethodChoices(models.TextChoices):
    """
    Enum-like class for representing payment method choices in a Django model.

    Attributes:
        CARD (str): Credit or Debit Card.
        BANK_TRANSFER (str): Bank Transfer.
        PAYPAL (str): PayPal payment.
        CRYPTO (str): Cryptocurrency payment.
    """

    CARD = "card", "Card"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    USSD = "ussd", "USSD"
