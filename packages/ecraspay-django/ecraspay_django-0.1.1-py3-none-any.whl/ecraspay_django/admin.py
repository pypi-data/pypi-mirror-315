from django.contrib import admin

from ecraspay_django.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    """
    Admin view for the Payment model.
    """

    list_display = ("id", "amount", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "status")
    readonly_fields = ("id", "created_at")


admin.site.register(Payment, PaymentAdmin)
