from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Brand, Vehicle, Product
from .forms import CategoryForm, BrandForm, VehicleForm, ProductForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


def get_user_role(user):
    if user.is_superuser:
        return 'super_admin'

    profile = getattr(user, 'userprofile', None)
    if profile:
        return profile.role

    return None


def dashboard_context():
    return {
        'products': Product.objects.count(),
        'categories': Category.objects.count(),
        'brands': Brand.objects.count(),
        'vehicles': Vehicle.objects.count(),
        'low_stock_products': Product.objects.filter(stock_quantity__lte=5).count(),
        'latest_products': Product.objects.select_related('category', 'brand').order_by('-created_at')[:5],
        'users': User.objects.count(),
        'super_admins': User.objects.filter(userprofile__role='super_admin').count(),
        'managers': User.objects.filter(userprofile__role='manager').count(),
        'inventory_staff': User.objects.filter(userprofile__role='inventory').count(),
        'sales_staff': User.objects.filter(userprofile__role='sales').count(),
    }


def role_dashboard(request, expected_role, template_name):
    if get_user_role(request.user) != expected_role:
        raise PermissionDenied

    return render(request, template_name, dashboard_context())


@login_required
def dashboard_redirect(request):
    role = get_user_role(request.user)
    dashboard_routes = {
        'super_admin': 'super_admin_dashboard',
        'manager': 'manager_dashboard',
        'inventory': 'inventory_dashboard',
        'sales': 'sales_dashboard',
    }
    return redirect(dashboard_routes.get(role, 'product_list'))


@login_required
def super_admin_dashboard(request):
    return role_dashboard(
        request,
        'super_admin',
        'dashboards/super_admin.html'
    )


@login_required
def manager_dashboard(request):
    return role_dashboard(
        request,
        'manager',
        'dashboards/manager.html'
    )


@login_required
def inventory_dashboard(request):
    return role_dashboard(
        request,
        'inventory',
        'dashboards/inventory.html'
    )


@login_required
def sales_dashboard(request):
    return role_dashboard(
        request,
        'sales',
        'dashboards/sales.html'
    )



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
# Create your views here.


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

@login_required
@permission_required('tailapp.add_category', raise_exception=True)
def add_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'category/add.html', {'form': form})

@login_required
@permission_required('tailapp.view_category', raise_exception=True)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})

@login_required
@permission_required('tailapp.change_category', raise_exception=True)
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'category/edit.html', {'form': form})

@login_required
@permission_required('tailapp.delete_category', raise_exception=True)
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('category_list')

@login_required
@permission_required('tailapp.add_brand', raise_exception=True)
def add_brand(request):
    form = BrandForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('brand_list')

    return render(request, 'brand/add.html', {'form': form})

@login_required
@permission_required('tailapp.view_brand', raise_exception=True)
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brand/list.html', {'brands': brands})

@login_required
@permission_required('tailapp.change_brand', raise_exception=True)
def edit_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    form = BrandForm(request.POST or None, instance=brand)

    if form.is_valid():
        form.save()
        return redirect('brand_list')

    return render(request, 'brand/edit.html', {'form': form})

@login_required
@permission_required('tailapp.delete_brand', raise_exception=True)
def delete_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    brand.delete()
    return redirect('brand_list')

@login_required
@permission_required('tailapp.add_vehicle', raise_exception=True)
def add_vehicle(request):
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vehicle_list')

    return render(request, 'vehicle/add.html', {'form': form})

@login_required
@permission_required('tailapp.view_vehicle', raise_exception=True)
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle/list.html', {'vehicles': vehicles})

@login_required
@permission_required('tailapp.change_vehicle', raise_exception=True)
def edit_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    form = VehicleForm(request.POST or None, instance=vehicle)

    if form.is_valid():
        form.save()
        return redirect('vehicle_list')

    return render(request, 'vehicle/edit.html', {'form': form})

@login_required
@permission_required('tailapp.delete_vehicle', raise_exception=True)
def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    vehicle.delete()
    return redirect('vehicle_list')

@login_required
@permission_required('tailapp.add_product', raise_exception=True)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product/add.html', {'form': form})

@login_required
@permission_required('tailapp.view_product', raise_exception=True)
def product_list(request):
    products = Product.objects.select_related('category', 'brand').prefetch_related('vehicle')
    return render(request, 'product/list.html', {'products': products})


@login_required
@permission_required('tailapp.change_product', raise_exception=True)
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product/edit.html', {'form': form})

@login_required
@permission_required('tailapp.delete_product', raise_exception=True)
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product_list')
