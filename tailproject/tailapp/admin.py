from django.contrib import admin

from .models import Brand, Category, Product, UserProfile, Vehicle


admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Vehicle)
admin.site.register(Product)
