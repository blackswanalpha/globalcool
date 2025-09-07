#!/usr/bin/env python
"""
Simple script to populate Global Cool-Light E.A LTD database with real HVAC data
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.services.models import Service, ServiceCategory
from apps.leads.models import Client, Booking, Inquiry

def create_services():
    """Create realistic HVAC services"""
    
    # Create categories
    categories_data = [
        {'name': 'Air Conditioning', 'slug': 'air-conditioning', 'description': 'Complete air conditioning solutions', 'icon': 'fas fa-snowflake'},
        {'name': 'Heating Systems', 'slug': 'heating-systems', 'description': 'Professional heating system services', 'icon': 'fas fa-fire'},
        {'name': 'Ventilation', 'slug': 'ventilation', 'description': 'Indoor air quality solutions', 'icon': 'fas fa-wind'},
        {'name': 'Commercial HVAC', 'slug': 'commercial-hvac', 'description': 'Commercial HVAC solutions', 'icon': 'fas fa-building'},
        {'name': 'Emergency Services', 'slug': 'emergency-services', 'description': '24/7 emergency HVAC services', 'icon': 'fas fa-exclamation-triangle'}
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = ServiceCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categories[cat_data['slug']] = category
        print(f"✅ Category: {category.name}")
    
    # Create services
    services_data = [
        {
            'category': 'air-conditioning',
            'name': 'Split AC Installation',
            'slug': 'split-ac-installation',
            'summary': 'Professional split air conditioner installation with warranty',
            'description': 'Complete split AC installation service including site assessment, professional installation, electrical connections, system testing, and 2-year warranty.',
            'base_price_min': 35000,
            'base_price_max': 85000,
            'duration_estimate': '4-8',
            'features': 'Professional installation\n2-year warranty\nFree maintenance check\nLoad calculation\nElectrical safety compliance'
        },
        {
            'category': 'air-conditioning',
            'name': 'Central AC Installation',
            'slug': 'central-ac-installation',
            'summary': 'Complete central air conditioning system installation',
            'description': 'Comprehensive central AC installation including system design, ductwork installation, professional equipment installation, and 3-year warranty.',
            'base_price_min': 150000,
            'base_price_max': 500000,
            'duration_estimate': '2-3-days',
            'features': 'Custom system design\nProfessional ductwork\n3-year warranty\nEnergy-efficient options\nSmart controls'
        },
        {
            'category': 'air-conditioning',
            'name': 'AC Repair & Maintenance',
            'slug': 'ac-repair-maintenance',
            'summary': 'Expert AC repair and preventive maintenance services',
            'description': 'Professional AC repair and maintenance including system diagnosis, refrigerant services, compressor repairs, and preventive maintenance plans.',
            'base_price_min': 3500,
            'base_price_max': 25000,
            'duration_estimate': '2-4',
            'features': 'Same-day service\nComprehensive diagnosis\nGenuine parts\n90-day warranty\nMaintenance plans'
        },
        {
            'category': 'heating-systems',
            'name': 'Heat Pump Installation',
            'slug': 'heat-pump-installation',
            'summary': 'Energy-efficient heat pump systems for year-round comfort',
            'description': 'Professional heat pump installation with site evaluation, high-efficiency equipment, and 5-year manufacturer warranty.',
            'base_price_min': 120000,
            'base_price_max': 300000,
            'duration_estimate': '1-day',
            'features': 'Energy-efficient\nProfessional sizing\n5-year warranty\nSmart controls\nEco-friendly refrigerants'
        },
        {
            'category': 'ventilation',
            'name': 'Exhaust Fan Installation',
            'slug': 'exhaust-fan-installation',
            'summary': 'Professional exhaust fan installation for kitchens and bathrooms',
            'description': 'Complete exhaust fan installation with proper sizing, professional ducting, electrical connections, and weatherproofing.',
            'base_price_min': 8000,
            'base_price_max': 25000,
            'duration_estimate': '2-4',
            'features': 'Proper sizing\nProfessional ducting\nNoise reduction\nWeatherproof installation\n1-year warranty'
        },
        {
            'category': 'commercial-hvac',
            'name': 'Office HVAC Systems',
            'slug': 'office-hvac-systems',
            'summary': 'Complete HVAC solutions for office buildings',
            'description': 'Comprehensive commercial HVAC services including system design, VRF/VRV installation, building automation, and maintenance contracts.',
            'base_price_min': 500000,
            'base_price_max': 2000000,
            'duration_estimate': '1-week',
            'features': 'Custom design\nVRF/VRV systems\nBuilding automation\nMaintenance contracts\nEnergy management'
        },
        {
            'category': 'emergency-services',
            'name': '24/7 Emergency HVAC Repair',
            'slug': 'emergency-hvac-repair',
            'summary': 'Urgent HVAC repair services available 24/7',
            'description': 'Emergency HVAC repair with 24/7 availability, rapid 2-hour response, emergency diagnostics, and temporary solutions.',
            'base_price_min': 5000,
            'base_price_max': 50000,
            'duration_estimate': '2-4',
            'features': '24/7 availability\n2-hour response\nEmergency diagnostics\nTemporary solutions\nPriority parts'
        }
    ]
    
    services = []
    for service_data in services_data:
        category_slug = service_data.pop('category')
        service_data['category'] = categories[category_slug]
        service_data['is_active'] = True
        
        service, created = Service.objects.get_or_create(
            slug=service_data['slug'],
            defaults=service_data
        )
        services.append(service)
        print(f"✅ Service: {service.name}")
    
    return services

def create_sample_data(services):
    """Create sample clients and bookings"""
    
    # Create sample clients
    clients_data = [
        {'name': 'Sarah Wanjiku', 'email': 'sarah.wanjiku@gmail.com', 'phone': '+254712345678', 'address': 'Kileleshwa, Nairobi'},
        {'name': 'David Kimani', 'email': 'david.kimani@yahoo.com', 'phone': '+254723456789', 'address': 'Karen, Nairobi'},
        {'name': 'TechHub Kenya Ltd', 'email': 'facilities@techhub.co.ke', 'phone': '+254734567890', 'address': 'Westlands, Nairobi', 'client_type': 'business'},
        {'name': 'Grace Muthoni', 'email': 'grace.muthoni@outlook.com', 'phone': '+254745678901', 'address': 'Runda, Nairobi'},
        {'name': 'Savannah Restaurant', 'email': 'manager@savannahrestaurant.co.ke', 'phone': '+254756789012', 'address': 'Kilimani, Nairobi', 'client_type': 'business'}
    ]
    
    clients = []
    for client_data in clients_data:
        client, created = Client.objects.get_or_create(
            email=client_data['email'],
            defaults=client_data
        )
        clients.append(client)
        print(f"✅ Client: {client.name}")
    
    # Create sample bookings
    bookings_data = [
        {
            'service': services[0],  # Split AC Installation
            'client': clients[0],
            'contact_name': 'Sarah Wanjiku',
            'contact_email': 'sarah.wanjiku@gmail.com',
            'contact_phone': '+254712345678',
            'preferred_date': date.today() + timedelta(days=3),
            'preferred_time_slot': '08:00-10:00',
            'location_address': 'House No. 45, Kileleshwa Drive, Nairobi',
            'message': 'Need split AC installation in master bedroom',
            'status': 'confirmed',
            'priority': 'normal',
            'source': 'website',
            'estimated_cost': Decimal('45000.00')
        },
        {
            'service': services[2],  # AC Repair
            'client': clients[1],
            'contact_name': 'David Kimani',
            'contact_email': 'david.kimani@yahoo.com',
            'contact_phone': '+254723456789',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time_slot': '14:00-16:00',
            'location_address': 'Karen Estate, Plot 12, Nairobi',
            'message': 'AC not cooling properly. Urgent repair needed.',
            'status': 'in_progress',
            'priority': 'high',
            'source': 'phone',
            'estimated_cost': Decimal('8500.00')
        },
        {
            'service': services[5],  # Office HVAC
            'client': clients[2],
            'contact_name': 'TechHub Facilities Manager',
            'contact_email': 'facilities@techhub.co.ke',
            'contact_phone': '+254734567890',
            'preferred_date': date.today() + timedelta(days=14),
            'preferred_time_slot': '08:00-10:00',
            'location_address': 'TechHub Building, Westlands Square, Nairobi',
            'message': 'Complete HVAC system for new 3-floor office building',
            'status': 'new',
            'priority': 'normal',
            'source': 'email',
            'estimated_cost': Decimal('750000.00')
        },
        {
            'service': services[6],  # Emergency Repair
            'client': clients[4],
            'contact_name': 'Restaurant Manager',
            'contact_email': 'manager@savannahrestaurant.co.ke',
            'contact_phone': '+254756789012',
            'preferred_date': date.today() - timedelta(days=2),
            'preferred_time_slot': '16:00-18:00',
            'location_address': 'Savannah Restaurant, Kilimani Plaza, Nairobi',
            'message': 'Kitchen exhaust system failed. Emergency repair needed.',
            'status': 'completed',
            'priority': 'urgent',
            'source': 'phone',
            'estimated_cost': Decimal('15000.00'),
            'actual_cost': Decimal('12500.00')
        }
    ]
    
    bookings = []
    for booking_data in bookings_data:
        # Check if booking already exists
        existing = Booking.objects.filter(
            contact_email=booking_data['contact_email'],
            service=booking_data['service']
        ).first()
        
        if not existing:
            booking = Booking.objects.create(**booking_data)
            bookings.append(booking)
            print(f"✅ Booking: {booking.contact_name} - {booking.service.name}")
        else:
            bookings.append(existing)
            print(f"✅ Booking exists: {existing.contact_name} - {existing.service.name}")
    
    # Create sample inquiries
    inquiries_data = [
        {
            'service': services[1],  # Central AC
            'contact_name': 'Peter Ochieng',
            'contact_email': 'peter.ochieng@gmail.com',
            'contact_phone': '+254767890123',
            'subject': 'Central AC Quote for 4-bedroom house',
            'message': 'I need a quote for central AC installation in my 4-bedroom house in Lavington. The house is about 300 sqm.',
            'budget_range': 'KSh 200,000 - 300,000',
            'timeline': 'Within 2 months',
            'priority': 'normal'
        },
        {
            'service': services[3],  # Heat Pump
            'contact_name': 'Linda Akinyi',
            'contact_email': 'linda.akinyi@outlook.com',
            'contact_phone': '+254778901234',
            'subject': 'Heat Pump System Quote',
            'message': 'Looking for an energy-efficient heating and cooling solution for my new home in Nakuru.',
            'budget_range': 'KSh 150,000 - 250,000',
            'timeline': 'Next month',
            'priority': 'normal',
            'status': 'in_review'
        }
    ]
    
    inquiries = []
    for inquiry_data in inquiries_data:
        inquiry, created = Inquiry.objects.get_or_create(
            contact_email=inquiry_data['contact_email'],
            defaults=inquiry_data
        )
        inquiries.append(inquiry)
        print(f"✅ Inquiry: {inquiry.contact_name} - {inquiry.subject}")
    
    return clients, bookings, inquiries

def main():
    """Main function to populate data"""
    print("🚀 Populating Global Cool-Light E.A LTD with real HVAC data...")
    print("=" * 60)
    
    # Create services
    services = create_services()
    
    # Create sample data
    clients, bookings, inquiries = create_sample_data(services)
    
    print("=" * 60)
    print("✅ Database populated successfully!")
    print(f"📊 Summary:")
    print(f"   • {len(services)} HVAC services")
    print(f"   • {len(clients)} sample clients")
    print(f"   • {len(bookings)} sample bookings")
    print(f"   • {len(inquiries)} sample inquiries")
    print()
    print("🌐 Access URLs:")
    print("   Booking: http://127.0.0.1:8000/booking/")
    print("   Services: http://127.0.0.1:8000/services/")
    print("   Admin: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    main()
