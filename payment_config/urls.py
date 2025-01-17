from django.urls import path

from payment_config import views


urlpatterns = [
    #path('get-bcv/', views.GetBCVView.as_view(), name="get_bcv"),
    path('get-iva/', views.GetIVAView.as_view(), name="get_iva"),
    #path('get-payment-methods/', views.ListPaymentMethodsView.as_view(),
    #     name="get_payment_methods"),
    path('get-all-payment-data', views.GetAllPaymentDataView.as_view(),
         name="get_all_payment_data"),
]
