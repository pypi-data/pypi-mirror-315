import uuid
from django.db import models
from .choices import PaymentStatusChoices, CurrencyChoices


class Payment(models.Model):
    """
    A Django model representing payment information.

    This model stores details about a payment, including its unique references, amount,
    currency, status, and timestamps for creation and updates.

    Fields:
        id (UUIDField): Unique identifier for the payment.
        payment_reference (CharField): Unique reference identifier for the payment.
        transaction_reference (CharField): Unique reference identifier for the transaction.
        amount (DecimalField): The amount for the payment.
        currency (CharField): The currency used for the payment, chosen from CurrencyChoices.
        status (CharField): The current status of the payment, chosen from PaymentStatusChoices.
        created_at (DateTimeField): Timestamp when the payment record was created.
        updated_at (DateTimeField): Timestamp when the payment record was last updated.

    Meta:
        verbose_name (str): Human-readable name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.
        ordering (list): Default ordering by the `created_at` field in descending order.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Payment ID"
    )
    payment_reference = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Payment Reference",
        help_text="Unique reference for the payment.",
    )
    transaction_reference = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Transaction Reference",
        help_text="Unique reference for the transaction.",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Payment amount.",
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        verbose_name="Currency",
        help_text="Currency of the payment.",
    )
    status = models.CharField(
        max_length=255,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
        verbose_name="Payment Status",
        help_text="Current status of the payment.",
    )
    payment_method = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Payment Method",
        help_text="Method used for the payment.",
    )

    # Optional fields
    gateway_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Gateway Reference",
        help_text="Reference from the payment gateway.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the payment was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Timestamp when the payment was last updated.",
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]  # Default ordering by creation date, descending.
        indexes = [
            models.Index(fields=["payment_reference"]),
            models.Index(fields=["transaction_reference"]),
        ]

    def __str__(self):
        """
        Returns a string representation of the payment.

        Example:
            "Payment <payment_reference> - <status>"
        """
        return f"Payment {self.payment_reference} - {self.status}"


class AbstractPayment(models.Model):
    """
    Abstract base model for storing payment information.

    This model serves as a base class for other payment-related models. It defines
    core fields such as unique references, amount, status, and timestamps, which
    can be extended by child models.

    Fields:
        id (UUIDField): Unique identifier for the payment.
        payment_reference (CharField): Unique reference identifier for the payment.
        transaction_reference (CharField): Unique reference identifier for the transaction.
        amount (DecimalField): The amount for the payment.
        status (CharField): The current status of the payment.
        created_at (DateTimeField): Timestamp when the payment record was created.
        updated_at (DateTimeField): Timestamp when the payment record was last updated.

    Meta:
        abstract (bool): Specifies that this is an abstract model.
        ordering (list): Default ordering by the `created_at` field in descending order.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Payment ID"
    )
    payment_reference = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Payment Reference",
        help_text="Unique reference for the payment.",
    )
    transaction_reference = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Transaction Reference",
        help_text="Unique reference for the transaction.",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Payment amount.",
    )
    status = models.CharField(
        max_length=255,
        verbose_name="Payment Status",
        help_text="Current status of the payment.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the payment was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Timestamp when the payment was last updated.",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns a string representation of the abstract payment.

        Example:
            "Abstract Payment <payment_reference> - <status>"
        """
        return f"Abstract Payment {self.payment_reference} - {self.status}"
