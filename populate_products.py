#!/usr/bin/env python
"""
Script to populate sample products data
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.services.models import ProductCategory, Product

def create_sample_products():
    """Create sample products for testing"""
    print("Creating product categories...")
    
    # Create product categories
    ac_units, created = ProductCategory.objects.get_or_create(
        name="Air Conditioning Units",
        defaults={
            'description': "Complete AC units for residential and commercial use",
            'icon': "fas fa-snowflake",
            'order': 1
        }
    )
    
    parts, created = ProductCategory.objects.get_or_create(
        name="AC Parts & Components",
        defaults={
            'description': "Replacement parts and components for HVAC systems",
            'icon': "fas fa-cogs",
            'order': 2
        }
    )
    
    accessories, created = ProductCategory.objects.get_or_create(
        name="HVAC Accessories",
        defaults={
            'description': "Accessories and tools for HVAC systems",
            'icon': "fas fa-tools",
            'order': 3
        }
    )
    
    print("Creating sample products...")
    
    # Create sample products
    products_data = [
        {
            'category': ac_units,
            'name': "Split AC Unit 12000 BTU",
            'summary': "Energy-efficient split air conditioning unit perfect for medium-sized rooms",
            'description': "<p>High-performance split AC unit with inverter technology for optimal energy efficiency. Features quiet operation, multiple cooling modes, and remote control.</p>",
            'price': Decimal('45000.00'),
            'stock_quantity': 15,
            'stock_status': 'in_stock',
            'sku': 'AC-SPLIT-12K',
            'features': "Energy Star certified\nQuiet operation below 40dB\nRemote control included\n5-year warranty\nR410A refrigerant",
            'warranty': "5 years manufacturer warranty",
            'is_active': True,
            'is_featured': True
        },
        {
            'category': ac_units,
            'name': "Window AC Unit 18000 BTU",
            'summary': "Powerful window-mounted air conditioner for larger rooms",
            'description': "<p>Heavy-duty window AC unit with high cooling capacity. Perfect for large rooms and small offices.</p>",
            'price': Decimal('35000.00'),
            'sale_price': Decimal('32000.00'),
            'stock_quantity': 10,
            'stock_status': 'in_stock',
            'sku': 'AC-WINDOW-18K',
            'features': "18000 BTU cooling capacity\nDigital display\nTimer function\n3-year warranty",
            'warranty': "3 years manufacturer warranty",
            'is_active': True
        },
        {
            'category': parts,
            'name': "AC Compressor Universal",
            'summary': "High-quality replacement compressor compatible with most AC units",
            'description': "<p>Universal AC compressor suitable for various air conditioning systems. Built with durable materials for long-lasting performance.</p>",
            'price': Decimal('15000.00'),
            'stock_quantity': 8,
            'stock_status': 'in_stock',
            'sku': 'COMP-UNI-001',
            'features': "Universal compatibility\nHigh efficiency\nDurable construction\n2-year warranty",
            'warranty': "2 years manufacturer warranty",
            'is_active': True
        },
        {
            'category': parts,
            'name': "AC Filter Set (Pack of 4)",
            'summary': "Premium air filters for improved air quality and system efficiency",
            'description': "<p>High-quality air filters that improve indoor air quality while maintaining optimal system performance.</p>",
            'price': Decimal('2500.00'),
            'stock_quantity': 50,
            'stock_status': 'in_stock',
            'sku': 'FILTER-SET-4',
            'features': "HEPA filtration\nPack of 4 filters\nEasy installation\n6-month lifespan",
            'warranty': "1 year manufacturer warranty",
            'is_active': True,
            'is_featured': True
        },
        {
            'category': accessories,
            'name': "Digital Thermostat",
            'summary': "Smart programmable thermostat with WiFi connectivity",
            'description': "<p>Advanced digital thermostat with smartphone app control and energy-saving features.</p>",
            'price': Decimal('8500.00'),
            'stock_quantity': 25,
            'stock_status': 'in_stock',
            'sku': 'THERMO-SMART-01',
            'features': "WiFi connectivity\nSmartphone app\nProgrammable schedules\nEnergy reports",
            'warranty': "2 years manufacturer warranty",
            'is_active': True
        },
        {
            'category': accessories,
            'name': "AC Remote Control Universal",
            'summary': "Universal remote control compatible with most AC brands",
            'description': "<p>Universal remote control that works with most air conditioning brands and models.</p>",
            'price': Decimal('1200.00'),
            'stock_quantity': 0,
            'stock_status': 'out_of_stock',
            'sku': 'REMOTE-UNI-01',
            'features': "Universal compatibility\nEasy setup\nBacklit display\nBattery included",
            'warranty': "1 year manufacturer warranty",
            'is_active': True
        }
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"Created product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")
    
    print("\nSample products created successfully!")
    print(f"Total products: {Product.objects.count()}")
    print(f"Total categories: {ProductCategory.objects.count()}")

if __name__ == '__main__':
    create_sample_products()
