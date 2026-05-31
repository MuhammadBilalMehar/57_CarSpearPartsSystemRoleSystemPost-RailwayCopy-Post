from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission, User

from .models import Brand, Category, Product, Vehicle


class DeletePermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='inventory',
            password='password123'
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name='Filters')
        self.brand = Brand.objects.create(name='Toyota')
        self.vehicle = Vehicle.objects.create(
            name='Corolla',
            model='GLI',
            year=2020
        )
        self.product = Product.objects.create(
            name='Oil Filter',
            part_number='OF-001',
            category=self.category,
            brand=self.brand,
            purchase_price='100.00',
            sale_price='150.00',
            stock_quantity=10
        )
        self.product.vehicle.add(self.vehicle)

    def test_inventory_user_without_delete_permissions_cannot_delete_anything(self):
        delete_targets = (
            ('delete_category', self.category, Category),
            ('delete_brand', self.brand, Brand),
            ('delete_vehicle', self.vehicle, Vehicle),
            ('delete_product', self.product, Product),
        )

        for route_name, instance, model in delete_targets:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name, args=[instance.id]))

                self.assertEqual(response.status_code, 403)
                self.assertTrue(model.objects.filter(id=instance.id).exists())

    def test_user_with_delete_product_permission_can_delete_product(self):
        permissions = Permission.objects.filter(
            codename__in=['delete_product', 'view_product'],
            content_type__app_label='tailapp'
        )
        self.user.user_permissions.add(*permissions)

        response = self.client.get(reverse('delete_product', args=[self.product.id]))

        self.assertRedirects(response, reverse('product_list'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


class RoleAccessTests(TestCase):
    def create_user_with_role(self, role):
        user = User.objects.create_user(
            username=role,
            password='password123'
        )
        user.userprofile.role = role
        user.userprofile.save()
        return user

    def test_sales_role_is_view_only(self):
        user = self.create_user_with_role('sales')

        self.assertTrue(user.has_perm('tailapp.view_product'))
        self.assertFalse(user.has_perm('tailapp.add_product'))
        self.assertFalse(user.has_perm('tailapp.change_product'))
        self.assertFalse(user.has_perm('tailapp.delete_product'))

    def test_inventory_role_can_change_but_not_delete(self):
        user = self.create_user_with_role('inventory')

        self.assertTrue(user.has_perm('tailapp.add_product'))
        self.assertTrue(user.has_perm('tailapp.change_product'))
        self.assertFalse(user.has_perm('tailapp.delete_product'))

    def test_manager_role_can_delete_inventory_records(self):
        user = self.create_user_with_role('manager')

        self.assertTrue(user.has_perm('tailapp.delete_product'))
        self.assertTrue(user.has_perm('tailapp.delete_category'))

    def test_login_redirects_user_to_role_dashboard(self):
        user = self.create_user_with_role('sales')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(response, reverse('sales_dashboard'))
