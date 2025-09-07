from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class ServiceCategory(models.Model):
    """Categories for HVAC services"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Individual HVAC services"""
    DURATION_CHOICES = [
        ('1-2', '1-2 hours'),
        ('2-4', '2-4 hours'),
        ('4-8', '4-8 hours'),
        ('1-day', '1 day'),
        ('2-3-days', '2-3 days'),
        ('1-week', '1 week'),
        ('custom', 'Custom duration'),
    ]

    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = models.TextField(max_length=500, help_text="Brief description for listings")
    description = RichTextField(help_text="Detailed service description")

    # Pricing
    base_price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_note = models.CharField(max_length=200, blank=True, help_text="e.g., 'Starting from' or 'Per unit'")

    # Service details
    duration_estimate = models.CharField(max_length=20, choices=DURATION_CHOICES, blank=True)
    specifications = models.JSONField(default=dict, blank=True, help_text="Technical specifications as JSON")

    # Features
    features = models.TextField(blank=True, help_text="Key features, one per line")
    requirements = models.TextField(blank=True, help_text="Requirements or prerequisites")

    # SEO and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Tracking
    view_count = models.PositiveIntegerField(default=0)
    booking_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['-is_featured', 'category__order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    @property
    def price_range(self):
        """Return formatted price range"""
        if self.base_price_min and self.base_price_max:
            if self.base_price_min == self.base_price_max:
                return f"KSh {self.base_price_min:,.0f}"
            return f"KSh {self.base_price_min:,.0f} - {self.base_price_max:,.0f}"
        elif self.base_price_min:
            return f"From KSh {self.base_price_min:,.0f}"
        return "Contact for pricing"

    @property
    def features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []


class ServiceImage(models.Model):
    """Images for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/%Y/%m/')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Use as service thumbnail")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Image"
        verbose_name_plural = "Service Images"
        ordering = ['order', '-is_featured', 'created_at']

    def __str__(self):
        return f"{self.service.name} - {self.title or 'Image'}"


class ProductCategory(models.Model):
    """Categories for HVAC products"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Individual HVAC products"""
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = models.TextField(max_length=500, help_text="Brief description for listings")
    description = RichTextField(help_text="Detailed product description")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Sale/discounted price")
    price_note = models.CharField(max_length=200, blank=True, help_text="e.g., 'Per unit' or 'Installation included'")

    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')
    sku = models.CharField(max_length=100, unique=True, blank=True, help_text="Stock Keeping Unit")

    # Product details
    specifications = models.JSONField(default=dict, blank=True, help_text="Technical specifications as JSON")
    dimensions = models.CharField(max_length=100, blank=True, help_text="e.g., '50cm x 30cm x 20cm'")
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., '5.2 kg'")

    # Features
    features = models.TextField(blank=True, help_text="Key features, one per line")
    warranty = models.CharField(max_length=100, blank=True, help_text="e.g., '2 years manufacturer warranty'")

    # SEO and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Tracking
    view_count = models.PositiveIntegerField(default=0)
    order_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-is_featured', 'category__order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:product_detail', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        """Return current price (sale price if available, otherwise regular price)"""
        if self.sale_price:
            return self.sale_price
        return self.price

    @property
    def price_display(self):
        """Return formatted price display"""
        if self.current_price:
            return f"KSh {self.current_price:,.0f}"
        return "Contact for pricing"

    @property
    def is_on_sale(self):
        """Check if product is on sale"""
        return self.sale_price and self.price and self.sale_price < self.price

    @property
    def features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_status == 'in_stock' and self.stock_quantity > 0


class ProductImage(models.Model):
    """Images for products"""
    IMAGE_TYPES = [
        ('main', 'Main Image'),
        ('gallery', 'Gallery'),
        ('detail', 'Detail Shot'),
        ('installation', 'Installation'),
        ('other', 'Other'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='gallery')
    is_featured = models.BooleanField(default=False, help_text="Use as product thumbnail")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order', '-is_featured', 'created_at']

    def __str__(self):
        return f"{self.product.name} - {self.title or 'Image'}"
