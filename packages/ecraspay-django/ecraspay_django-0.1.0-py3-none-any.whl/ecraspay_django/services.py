from requests.exceptions import HTTPError
from ecraspay import Checkout, Transaction, Card, BankTransfer, USSD
from ecraspay_django.settings import get_ecraspay_setting
from django.apps import apps
import logging
from .choices import PaymentStatusChoices

logger = logging.getLogger(__name__)


class EcraspayService:
    def __init__(self):
        self.api_key = get_ecraspay_setting("ECRASPAY_API_KEY")
        self.environment = get_ecraspay_setting("ECRASPAY_ENVIRONMENT")
        self.redirect_url = get_ecraspay_setting("ECRAS_REDIRECT_URL")
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all Ecraspay services dynamically."""
        services = {
            "checkout": Checkout,
            "transaction": Transaction,
            "card": Card,
            "bank_transfer": BankTransfer,
            "ussd": USSD,
        }
        for name, service_class in services.items():
            setattr(
                self,
                name,
                service_class(api_key=self.api_key, environment=self.environment),
            )

    # Transaction Methods

    def initiate_transaction(
        self,
        amount,
        reference,
        customer_name,
        customer_email,
        redirect_url=None,
        description=None,
        fee_bearer=None,
        currency="usd",
        payment_method="card",
        customer_phone=None,
        metadata=None,
        **kwargs,
    ):
        """Initiates a new transaction and stores it in the database."""
        try:
            if redirect_url is None:
                redirect_url = self.redirect_url
            response = self.transaction.initiate_transaction(
                amount=amount,
                payment_reference=reference,
                customer_name=customer_name,
                customer_email=customer_email,
                redirect_url=redirect_url,
                description=description,
                fee_bearer=fee_bearer,
                currency=currency,
                payment_method=payment_method,
                customer_phone=customer_phone,
                metadata=metadata,
                **kwargs,
            )
            self._store_payment(
                transaction_reference=response["responseBody"]["transactionReference"],
                payment_reference=reference,
                currency=currency,
                amount=amount,
                status=PaymentStatusChoices.PENDING,
                metadata=metadata,
            )
            logger.info(f"Transaction {reference} initialized successfully")
            return response
        except HTTPError as e:
            logger.error(f"Failed to initiate transaction {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def get_transaction_details(self, reference):
        """Fetches details of a transaction."""
        try:
            response = self.transaction.get_transaction_details(reference)
            logger.info(f"Fetched details for transaction {reference}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to fetch details for transaction {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def verify_transaction(self, reference):
        """Verifies the status of a transaction."""
        try:
            response = self.transaction.verify_transaction(reference)
            logger.info(f"Transaction {reference} verified successfully")
            self._update_payment_status(reference, "verified")
            return response
        except HTTPError as e:
            logger.error(f"Failed to verify transaction {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def get_transaction_status(self, reference):
        """Fetches the status of a transaction."""
        try:
            response = self.transaction.get_transaction_status(reference)
            logger.info(f"Fetched status for transaction {reference}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to fetch status for transaction {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def cancel_transaction(self, reference):
        """Cancels a transaction."""
        try:
            response = self.transaction.cancel_transaction(reference)
            logger.info(f"Transaction {reference} canceled successfully")
            self._update_payment_status(reference, "canceled")
            return response
        except HTTPError as e:
            logger.error(f"Failed to cancel transaction {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    # Card Payment Methods

    def initiate_card_payment(self, transaction_ref, card_payload, device_details):
        """Initiates a card payment."""
        try:
            response = self.card.initiate_payment(
                card_payload=card_payload,
                transaction_ref=transaction_ref,
                device_details=device_details,
            )
            logger.info(f"Card payment initiated for transaction {transaction_ref}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to initiate card payment: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def submit_card_otp(self, otp, gateway_ref):
        """Submits an OTP for a card payment."""
        try:
            response = self.card.submit_otp(otp=otp, gateway_ref=gateway_ref)
            logger.info(f"OTP submitted for gateway reference {gateway_ref}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to submit OTP: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def resend_card_otp(self, gateway_ref):
        """Resends the OTP for a card payment."""
        try:
            response = self.card.resend_otp(gateway_ref=gateway_ref)
            logger.info(f"OTP resend requested for gateway reference {gateway_ref}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to resend OTP: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def get_card_payment_details(self, transaction_ref):
        """Retrieves details of a card transaction."""
        try:
            response = self.card.get_card_details(transaction_ref=transaction_ref)
            logger.info(f"Retrieved card details for transaction {transaction_ref}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to get card details: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def verify_card_payment(self, transaction_ref):
        """Verifies the status of a card payment."""
        try:
            response = self.card.verify_card_payment(transaction_ref=transaction_ref)
            logger.info(f"Card payment verified for transaction {transaction_ref}")
            self._update_payment_status(transaction_ref, "verified")
            return response
        except HTTPError as e:
            logger.error(f"Failed to verify card payment: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    # USSD Payment Methods

    def initiate_ussd_payment(self, transaction_ref, bank_name):
        """Initiates a USSD payment."""
        try:
            response = self.ussd.initiate_ussd_payment(
                bank_name=bank_name,
                transaction_ref=transaction_ref,
            )
            logger.info(f"USSD payment initiated for transaction {transaction_ref}")
            return response
        except HTTPError as e:
            logger.error(f"Failed to initiate USSD payment: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def get_ussd_supported_banks(self):
        """Retrieves the list of banks that support USSD payments."""
        try:
            response = self.ussd.get_bank_list()
            logger.info("Retrieved list of supported banks for USSD payments")
            return response
        except HTTPError as e:
            logger.error(f"Failed to retrieve supported banks for USSD: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    # Checkout Methods
    def initiate_checkout(
        self,
        amount,
        reference,
        customer_name,
        customer_email,
        redirect_url=None,
        description=None,
        fee_bearer=None,
        currency="usd",
        payment_method="card",
        customer_phone=None,
        metadata=None,
        **kwargs,
    ):
        """Initiates a new checkout and stores it in the database."""

        if redirect_url is None:
            redirect_url = self.redirect_url

        try:
            response = self.checkout.initiate_checkout(
                amount=amount,
                payment_reference=reference,
                customer_name=customer_name,
                customer_email=customer_email,
                redirect_url=redirect_url,
                description=description,
                fee_bearer=fee_bearer,
                currency=currency,
                payment_method=payment_method,
                customer_phone=customer_phone,
                metadata=metadata,
                **kwargs,
            )
            saved_data = self._store_payment(
                reference=reference,
                amount=amount,
                status="initialized",
                metadata=metadata,
            )
            logger.info(f"Checkout {reference} initialized successfully")
            return {
                "payment_link": response["responseBody"]["checkoutUrl"],
                "payment_data": saved_data,
            }
        except HTTPError as e:
            logger.error(f"Failed to initiate checkout {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise

    def verify_checkout(self, reference):
        """Verifies the status of a checkout."""
        try:
            response = self.checkout.verify_checkout(reference)
            logger.info(f"Checkout {reference} verified successfully")
            status =  if response["responseBody"] 
            self._update_payment_status(reference, )
            return response
        except HTTPError as e:
            logger.error(f"Failed to verify checkout {reference}: {e}")
            if e.response.status_code == 400:
                return e.response.json()
            raise  # Re-raise the exception to the caller

    # Utility Methods

    def _store_payment(self, reference, amount, status, metadata=None):
        """Stores payment data in the configured model."""
        try:
            payment_model = apps.get_model(
                get_ecraspay_setting("ECRASPAY_PAYMENT_STORAGE")
            )
            payment = payment_model.objects.create(
                reference=reference,
                amount=amount,
                status=status,
                metadata=metadata or {},
            )
            logger.info(f"Payment {reference} stored successfully")
            return payment
        except Exception as e:
            logger.error(f"Failed to store payment {reference}: {e}")
            raise

    def _update_payment_status(self, reference, status):
        """Updates the status of a payment in the database."""
        try:
            payment_model = apps.get_model(
                get_ecraspay_setting("ECRASPAY_PAYMENT_STORAGE")
            )
            payment = payment_model.objects.get(reference=reference)
            payment.status = status
            payment.save()
            logger.info(f"Payment {reference} status updated to {status}")
            return payment
        except payment_model.DoesNotExist:
            logger.error(f"Payment {reference} not found in the database")
            raise ValueError(f"Payment {reference} not found")
        except Exception as e:
            logger.error(f"Failed to update payment status for {reference}: {e}")
            raise
