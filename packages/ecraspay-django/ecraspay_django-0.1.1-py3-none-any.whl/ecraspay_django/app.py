from django.apps import AppConfig


class EcraspayDjangoConfig(AppConfig):
    """
    App configuration for the ecraspay_django package.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "ecraspay_django"
    verbose_name = "Ecraspay Django Integration"

    def ready(self):
        """
        Hook for application initialization.
        Import signals or other startup code here.
        """
        import ecraspay_django.signals  # Import custom signals
