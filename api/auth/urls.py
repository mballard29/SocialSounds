from django.urls import path
from . import views as auth_views

urlpatterns = [
    path('me/', auth_views.UserView.as_view(), name='user'),
    path('me/profile/', auth_views.ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', auth_views.RegisterView.as_view(), name='register')
]