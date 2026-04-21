from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Sum
from datetime import date, timedelta
from .models import Producto, Venta, Perfil
from .forms import ProductoForm, VentaForm  # lo crearemos luego
from django.contrib import messages


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permiso para acceder.')
            return redirect('index')
    return wrapper

@login_required
def index(request):
    return render(request, 'farmacia/index.html')

@login_required
def productos(request):
    # empleados ven todos los productos, pero sin botones de edición
    productos = Producto.objects.all()
    return render(request, 'farmacia/productos_list.html', {'productos': productos})

@admin_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado.')
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'farmacia/producto_form.html', {'form': form})

@admin_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado.')
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'farmacia/producto_form.html', {'form': form})

@admin_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('productos')
    return render(request, 'farmacia/confirmar_eliminar.html', {'producto': producto})


#vista nueva venta 
@login_required
def nueva_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            if producto.stock >= cantidad:
                # Restar stock
                producto.stock -= cantidad
                producto.save()
                # Crear venta (sin subtotal, se calculará automáticamente si usamos save en modelo)
                venta = form.save(commit=False)
                venta.subtotal = producto.precio * cantidad
                venta.vendedor = request.user
                venta.save()
                messages.success(request, 'Venta registrada correctamente.')
                return redirect('lista_ventas')
            else:
                messages.error(request, f'Stock insuficiente. Solo hay {producto.stock} unidades.')
    else:
        form = VentaForm()
    return render(request, 'farmacia/nueva_venta.html', {'form': form})


#Lista de ventas (solo admin puede ver todas; empleado solo las suyas):
@login_required
def lista_ventas(request):
    if request.user.perfil.rol == 'admin':
        ventas = Venta.objects.all().order_by('-fecha')
    else:
        ventas = Venta.objects.filter(vendedor=request.user).order_by('-fecha')
    return render(request, 'farmacia/lista_ventas.html', {'ventas': ventas})

#ultimafuncionalidad dashboard

@admin_required
def dashboard(request):
    hoy = date.today()
    proximo_limite = hoy + timedelta(days=30)
    productos_proximos = Producto.objects.filter(fecha_vencimiento__lte=proximo_limite).order_by('fecha_vencimiento')
    # estadísticas
    total_productos = Producto.objects.count()
    stock_bajo = Producto.objects.filter(stock__lt=5).count()
    ventas_hoy = Venta.objects.filter(fecha__date=hoy).count()
    return render(request, 'farmacia/dashboard.html', {
        'productos_proximos': productos_proximos,
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'ventas_hoy': ventas_hoy,
    })