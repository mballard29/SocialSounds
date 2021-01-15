from django.contrib import admin
from django.urls import include, path
from api.auth import views as auth_views


urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='login'),
]