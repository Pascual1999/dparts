from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrdersList.as_view(), name="order_list"),
    path('orders/<int:pk>/', views.GetOrder.as_view(), name="get_order"),
    path('new-order/', views.CreateOrder.as_view(), name="new_order"),
    path('upload-payment/<int:pk>/', views.UpdateOrder.as_view(),
         name="update_order"),
    path('cancel-payment/<int:pk>/', views.CancelOrder.as_view(),
         name="cancel_order"),
]
