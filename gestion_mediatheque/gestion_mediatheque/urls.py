from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Homepage

urlpatterns = [
    path('', Homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('bibliothecaire/', include('bibliothecaire.urls')),
    path('membre/', include('membre.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/membre/'), name='logout'),
]