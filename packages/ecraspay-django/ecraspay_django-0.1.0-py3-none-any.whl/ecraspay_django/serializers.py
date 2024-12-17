from rest_framework import serializers
from .services import EcraspayService
from .choices import CurrencyChoices


import random
import string
from datetime import datetime


def payment_reference_generator():
    """
    Generate a unique and human-readable payment reference.

    Format: PREFIX + YYYYMMDD + RANDOM 6-CHAR ALPHANUMERIC

    Returns:
        str: A unique payment reference.
    """
    # Define a prefix (e.g., "PAY" for payment)
    prefix = "PAY"

    # Add a timestamp (YYYYMMDD) for date-based uniqueness
    date_str = datetime.now().strftime("%Y%m%d")

    # Generate a random 6-character alphanumeric string
    random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Combine all parts into a single reference
    payment_ref = f"{prefix}-{date_str}-{random_str}"

    return payment_ref


# Example Usage
print(payment_reference_generator())


class PaymentInitiationSerializer(serializers.Serializer):
    """
    A Django REST framework serializer to validate incoming payment initiation requests.
    """

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default=CurrencyChoices.NGN)
    description = serializers.CharField(max_length=100)
    metadata = serializers.DictField(required=False)

    def validate(self, attrs):
        if attrs["amount"] <= 100:
            raise serializers.ValidationError("Amount must be greater than 100.")

        return attrs

    def create(self, validated_data):
        payment_reference = payment_reference_generator()
        amount = validated_data["amount"]
        currency = validated_data["currency"]
        description = validated_data["description"]
        metadata = validated_data.get("metadata")
        email = metadata.get("email")

        # Initiate payment using the EcraspayService
        ecraspay_service = EcraspayService()
        try:
            response = ecraspay_service.initiate_checkout(
                amount=amount,
                currency=currency,
                description=description,
                payment_reference=payment_reference,
                metadata=metadata,
                email=email,
            )
        except Exception as e:
            raise serializers.ValidationError(str(e))

        payment_link = response["responseBody"]["checkoutUrl"]

        return 
