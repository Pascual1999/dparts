from django.urls import path

from users import views

from knox import views as knox_views

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name="signup"),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name="change-password"),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(),
         name='knox_logoutall'),
]
