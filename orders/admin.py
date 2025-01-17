from django.contrib import admin
from django.conf import settings
from .models import Order, OrderItem
from django_apscheduler.models import DjangoJob, DjangoJobExecution


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'product_name', 'quantity', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status',
                    'amount', 'amount_VEF',
                    'exchange_rate', 'created_at',
                    'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ("Información del cliente", {
            "fields": (
                'user',
                'payment_method',
                'shipping_address',
                'contact_number',

                'created_at',
                'updated_at',
            )}
        ),
        ("Información de pago", {
            "fields": (
                'status',
                'IVA',
                'amount',
                'amount_VEF',
                'exchange_rate',
                'proof_of_payment',
            )}
        ),
        )
    readonly_fields = ('user', 'IVA', 'amount', 'amount_VEF', 'exchange_rate', 'created_at', 'updated_at')
    search_fields = ['id', 'status']
    list_filter = ['status', 'created_at', 'updated_at']
    list_per_page = 20


admin.site.index_template = 'admin/customIndex.html'
admin.site.site_url = settings.SITE_URL

# Cancelar registro de los modelos DjangoJob and DjangoJobExecution
admin.site.unregister(DjangoJob)
admin.site.unregister(DjangoJobExecution)
