from django.contrib import admin

# Register your models here.

from .models import DollarExchangeHistory, PaymentConfig, PaymentMethod

admin.site.register(PaymentMethod)
admin.site.register(PaymentConfig)
admin.site.register(DollarExchangeHistory)