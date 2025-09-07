#!/usr/bin/env python
"""
Script to create sample categories for testing the Categories tab.
Run this with: python manage.py shell < scripts/create_sample_categories.py
"""

from apps.services.models import ServiceCategory, ProductCategory

def create_sample_service_categories():
    """Create sample service categories"""
    service_categories = [
        {
            'name': 'Air Conditioning',
            'description': 'Complete AC installation, repair, and maintenance services',
            'order': 1,
            'is_active': True
        },
        {
            'name': 'Heating Systems',
            'description': 'Heating system installation and repair services',
            'order': 2,
            'is_active': True
        },
        {
            'name': 'Ventilation',
            'description': 'Ventilation system design and installation',
            'order': 3,
            'is_active': True
        },
        {
            'name': 'Maintenance',
            'description': 'Regular maintenance and inspection services',
            'order': 4,
            'is_active': True
        }
    ]
    
    for cat_data in service_categories:
        category, created = ServiceCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Created service category: {category.name}")
        else:
            print(f"📝 Service category already exists: {category.name}")

def create_sample_product_categories():
    """Create sample product categories"""
    product_categories = [
        {
            'name': 'AC Units',
            'description': 'Air conditioning units and systems',
            'order': 1,
            'is_active': True
        },
        {
            'name': 'Filters & Parts',
            'description': 'Replacement filters and spare parts',
            'order': 2,
            'is_active': True
        },
        {
            'name': 'Tools & Equipment',
            'description': 'Professional HVAC tools and equipment',
            'order': 3,
            'is_active': True
        }
    ]
    
    for cat_data in product_categories:
        category, created = ProductCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Created product category: {category.name}")
        else:
            print(f"📝 Product category already exists: {category.name}")

# Create the categories
print("Creating sample categories...")
print("\n=== Service Categories ===")
create_sample_service_categories()

print("\n=== Product Categories ===")
create_sample_product_categories()

print("\n=== Summary ===")
print(f"Total Service Categories: {ServiceCategory.objects.count()}")
print(f"Total Product Categories: {ProductCategory.objects.count()}")
print("✅ Sample categories created successfully!")
