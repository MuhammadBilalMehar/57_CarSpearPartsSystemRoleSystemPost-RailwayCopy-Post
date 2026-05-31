from django import forms
from .models import Category, Brand, Vehicle, Product, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            user.email = self.cleaned_data['email']
            user.save(update_fields=['email'])
            profile = user.userprofile
            profile.role = self.cleaned_data['role']
            profile.save(update_fields=['role'])

        return user


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'model', 'year']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'part_number',
            'category',
            'brand',
            'vehicle',
            'purchase_price',
            'sale_price',
            'stock_quantity',
            'description',
            'image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'part_number': forms.TextInput(attrs={'class': 'form-control'}),

            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.SelectMultiple(attrs={'class': 'form-control'}),

            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
