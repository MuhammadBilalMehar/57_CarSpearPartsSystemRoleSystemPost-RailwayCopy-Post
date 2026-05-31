from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('manager', 'Manager'),
        ('inventory','Inventory Staff'),
        ('sales', 'Sales Staff'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='inventory'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    image = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username
    

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    name = models.CharField(max_length=100)   # e.g., Toyota Corolla
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.model} - {self.year})"

class Product(models.Model):
    name = models.CharField(max_length=150)
    part_number = models.CharField(max_length=100, unique=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products'
    )

    vehicle = models.ManyToManyField(
        Vehicle,
        related_name='products'
    )

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.PositiveIntegerField(default=0)

    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.part_number}"
