# Ecraspay Django Package

A Django package for integrating with the **Ecraspay API**. This package provides functionalities for initiating and verifying payments, managing transactions, and simplifying payment workflows within Django applications.

## Features

- Initiate payments using the Ecraspay API.
- Verify payment status via polling.
- Support for multiple payment methods (Card, Bank Transfer, USSD).
- Predefined Django models for storing payment data.
- Easy integration with existing apps and workflows.

---

## Installation

1. **Install the package using `pip`**:
   ```bash
   pip install ecraspay-django
   ```

2. **Add the package to your Django project**:

   In your `settings.py`, add the package to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       ...,
       "ecraspay_django",
   ]
   ```

---

## Configuration

Add the following configuration to your `settings.py`:

```python
ECRASPAY_API_KEY = "your-ecraspay-api-key"  # Replace with your API key
ECRASPAY_ENVIRONMENT = "sandbox"  # "sandbox" or "production"
ECRAS_REDIRECT_URL = "https://yourdomain.com/payment/success"
PAYMENT_PROCESSING_MODE = "checkout"  # Default: "checkout"
```

If you're using environment variables, you can configure them as follows:

```bash
export ECRASPAY_API_KEY=your-api-key
export ECRASPAY_ENVIRONMENT=sandbox
export ECRAS_REDIRECT_URL=https://yourdomain.com/payment/success
```

---

## Models

This package includes the following models:

1. **Payment**  
   Represents a payment initiated using the Ecraspay API.
   - Fields: `payment_reference`, `transaction_reference`, `amount`, `status`, `currency`, etc.

2. **AbstractPayment**  
   Provides a base model for storing payments that can be extended by other apps.

### Example Usage:

```python
from ecraspay_django.models import Payment

# Example: Fetch a payment
payment = Payment.objects.get(payment_reference="PAY-20240405-ABC123")
print(payment.status, payment.amount)
```

---

## Payment Workflow

### 1. **Initiating a Payment**

To initiate a payment, use the `EcraspayService` class:

```python
from ecraspay_django.services import EcraspayService

# Initialize the service
service = EcraspayService()

# Initiate checkout
response = service.initiate_checkout(
    amount=1000.00,
    reference="PAY-20240405-ABC123",
    customer_name="John Doe",
    customer_email="johndoe@example.com",
    description="School Fee Payment",
    currency="NGN",
    metadata={"school": "ABC School"}
)

print("Payment Link:", response["payment_link"])
```

---

### 2. **Verifying a Payment**

To verify a payment, use the `verify_checkout` method:

```python
response = service.verify_checkout(reference="PAY-20240405-ABC123")
print("Payment Status:", response["responseBody"]["status"])
```

---

## Views and Endpoints

This package includes the following API endpoints:

| Method | Endpoint                   | Description                 |
|--------|----------------------------|-----------------------------|
| `POST` | `/payment/`                | Initiate a payment          |
| `GET`  | `/payment/verify/<id>/`    | Verify a payment status     |

---

## Signals

The package provides a **`webhook_received`** signal to handle webhook events (optional in future integration):

```python
from django.dispatch import receiver
from ecraspay_django.views import webhook_received

@receiver(webhook_received)
def handle_webhook(sender, request, event, **kwargs):
    print("Webhook event received:", event)
```

---

## Polling for Payment Verification

If you are not using webhooks, you can verify payments via polling. Use a periodic task scheduler like **Celery** or `cron` to check payment statuses.

### Example Polling Function

```python
from ecraspay_django.models import Payment
from ecraspay_django.services import EcraspayService

def verify_pending_payments():
    service = EcraspayService()
    pending_payments = Payment.objects.filter(status="PENDING")
    
    for payment in pending_payments:
        response = service.verify_checkout(payment.payment_reference)
        status = response["responseBody"].get("status")
        
        if status == "SUCCESS":
            payment.status = "COMPLETED"
        elif status == "FAILED":
            payment.status = "FAILED"
        payment.save()
        print(f"Payment {payment.payment_reference} updated to {payment.status}")
```

---

## URL Configuration

Add the following URLs to your project's `urls.py`:

```python
from django.urls import path
from ecraspay_django.views import PaymentView, PaymentVerificationView

urlpatterns = [
    path("payment/", PaymentView.as_view(), name="payment"),
    path("payment/verify/<str:payment_id>/", PaymentVerificationView.as_view(), name="payment-verification"),
]
```

---

## Utilities

### Generate a Payment Reference:

```python
from ecraspay_django.utils import payment_reference_generator

reference = payment_reference_generator()
print(reference)  # e.g., PAY-20240405-ABC123
```

---

## Contribution Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecraspay-django.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   python manage.py test
   ```

4. Submit a pull request for improvements or bug fixes.

---

## License

This package is released under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## Contact

For questions or contributions:
- **Email**: `sammyboy.as@gmail.com`
- **GitHub**: [Your GitHub Profile](https://github.com/thelimeskies)

---
