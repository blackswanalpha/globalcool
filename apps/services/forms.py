from django import forms
from django.forms import inlineformset_factory
from .models import Service, ServiceCategory, ServiceImage, Product, ProductCategory, ProductImage


class ServiceForm(forms.ModelForm):
    """Form for creating and editing services"""
    
    class Meta:
        model = Service
        fields = [
            'category', 'name', 'summary', 'description',
            'base_price_min', 'base_price_max', 'price_note',
            'duration_estimate', 'features', 'requirements',
            'is_active', 'is_featured', 'meta_title', 'meta_description'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service name',
                'required': True
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description for listings (max 500 characters)',
                'maxlength': 500
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Detailed service description'
            }),
            'base_price_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum price (KSh)',
                'step': '0.01'
            }),
            'base_price_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum price (KSh)',
                'step': '0.01'
            }),
            'price_note': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "Starting from" or "Per unit"'
            }),
            'duration_estimate': forms.Select(attrs={
                'class': 'form-control'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Key features, one per line'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Requirements or prerequisites'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (max 60 characters)',
                'maxlength': 60
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (max 160 characters)',
                'maxlength': 160
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ServiceCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select a category"


class ProductForm(forms.ModelForm):
    """Form for creating and editing products"""
    
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'summary', 'description',
            'price', 'sale_price', 'price_note',
            'stock_quantity', 'stock_status', 'sku',
            'dimensions', 'weight', 'features', 'warranty',
            'is_active', 'is_featured', 'meta_title', 'meta_description'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
                'required': True
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description for listings (max 500 characters)',
                'maxlength': 500
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Detailed product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Regular price (KSh)',
                'step': '0.01'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sale price (KSh)',
                'step': '0.01'
            }),
            'price_note': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "Per unit" or "Installation included"'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock quantity',
                'min': 0
            }),
            'stock_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock Keeping Unit (SKU)'
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "50cm x 30cm x 20cm"'
            }),
            'weight': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "5.2 kg"'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Key features, one per line'
            }),
            'warranty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "2 years manufacturer warranty"'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (max 60 characters)',
                'maxlength': 60
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (max 160 characters)',
                'maxlength': 160
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select a category"

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        sale_price = cleaned_data.get('sale_price')
        
        if sale_price and price and sale_price >= price:
            raise forms.ValidationError("Sale price must be less than regular price.")
        
        return cleaned_data


class ServiceImageForm(forms.ModelForm):
    """Form for service images"""
    
    class Meta:
        model = ServiceImage
        fields = ['image', 'title', 'description', 'is_featured']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Image description'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ProductImageForm(forms.ModelForm):
    """Form for product images"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'title', 'description', 'is_featured']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Image description'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# Inline formsets for images
ServiceImageFormSet = inlineformset_factory(
    Service, ServiceImage, form=ServiceImageForm,
    extra=1, can_delete=True, max_num=10
)

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm,
    extra=1, can_delete=True, max_num=10
)
