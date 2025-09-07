#!/usr/bin/env python
"""
Quick script to delete services and products data.
Run this with: python manage.py shell < scripts/delete_services_products.py
"""

from django.db import transaction
from apps.services.models import (
    Service, ServiceCategory, ServiceImage,
    Product, ProductCategory, ProductImage
)

def show_current_counts():
    """Display current data counts"""
    print("=== Current Database Counts ===")
    print(f"Service Categories: {ServiceCategory.objects.count()}")
    print(f"Services: {Service.objects.count()}")
    print(f"Service Images: {ServiceImage.objects.count()}")
    print(f"Product Categories: {ProductCategory.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Product Images: {ProductImage.objects.count()}")
    print()

def delete_all_services_products():
    """Delete all services and products data"""
    print("Starting deletion of all services and products data...")
    
    try:
        with transaction.atomic():
            # Delete in proper order to avoid foreign key constraints
            service_images_deleted = ServiceImage.objects.all().delete()
            product_images_deleted = ProductImage.objects.all().delete()
            services_deleted = Service.objects.all().delete()
            products_deleted = Product.objects.all().delete()
            service_cats_deleted = ServiceCategory.objects.all().delete()
            product_cats_deleted = ProductCategory.objects.all().delete()
            
            print("=== Deletion Results ===")
            print(f"Service Images deleted: {service_images_deleted[0]}")
            print(f"Product Images deleted: {product_images_deleted[0]}")
            print(f"Services deleted: {services_deleted[0]}")
            print(f"Products deleted: {products_deleted[0]}")
            print(f"Service Categories deleted: {service_cats_deleted[0]}")
            print(f"Product Categories deleted: {product_cats_deleted[0]}")
            
            total_deleted = (
                service_images_deleted[0] + product_images_deleted[0] +
                services_deleted[0] + products_deleted[0] +
                service_cats_deleted[0] + product_cats_deleted[0]
            )
            
            print(f"\nTotal items deleted: {total_deleted}")
            print("✅ All services and products data deleted successfully!")
            
    except Exception as e:
        print(f"❌ Error during deletion: {e}")
        raise

def delete_services_only():
    """Delete only services and service images"""
    print("Deleting services and service images only...")
    
    try:
        with transaction.atomic():
            service_images_deleted = ServiceImage.objects.all().delete()
            services_deleted = Service.objects.all().delete()
            
            print(f"Service Images deleted: {service_images_deleted[0]}")
            print(f"Services deleted: {services_deleted[0]}")
            print("✅ Services data deleted successfully!")
            
    except Exception as e:
        print(f"❌ Error during deletion: {e}")
        raise

def delete_products_only():
    """Delete only products and product images"""
    print("Deleting products and product images only...")
    
    try:
        with transaction.atomic():
            product_images_deleted = ProductImage.objects.all().delete()
            products_deleted = Product.objects.all().delete()
            
            print(f"Product Images deleted: {product_images_deleted[0]}")
            print(f"Products deleted: {products_deleted[0]}")
            print("✅ Products data deleted successfully!")
            
    except Exception as e:
        print(f"❌ Error during deletion: {e}")
        raise

# Show current state
show_current_counts()

# Uncomment the function you want to run:

# Delete everything:
delete_all_services_products()

# Delete only services:
# delete_services_only()

# Delete only products:
# delete_products_only()

# Show final state
print("\n=== Final Database Counts ===")
show_current_counts()
