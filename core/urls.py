from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from farmacia import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='farmacia/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('ventas/nueva/', views.nueva_venta, name='nueva_venta'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('dashboard/', views.dashboard, name='dashboard'),
]