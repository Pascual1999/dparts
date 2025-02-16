from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', include('report.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include('product.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('payment_config.urls')),
    path('api-auth/', include('rest_framework.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
