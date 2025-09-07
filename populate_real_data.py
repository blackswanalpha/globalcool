#!/usr/bin/env python
"""
Populate Global Cool-Light E.A LTD database with real HVAC services and sample data
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
from apps.core.models import SiteSettings

def create_company_info():
    """Create company information"""
    try:
        company = SiteSettings.objects.get()
        print(f"✅ Site settings already exist")
    except SiteSettings.DoesNotExist:
        company = SiteSettings.objects.create(
            company_name="Global Cool-Light E.A LTD",
            tagline='Your Trusted HVAC Solutions Partner',
            description='Professional heating, ventilation, and air conditioning services across Kenya. We provide installation, maintenance, and repair services for residential and commercial properties.',
            phone='+254 712 345 678',
            email='info@globalcool-light.com',
            address='Westlands, Nairobi, Kenya',
            facebook_url='https://facebook.com/globalcoollight',
            twitter_url='https://twitter.com/globalcoollight',
            linkedin_url='https://linkedin.com/company/globalcoollight',
            instagram_url='https://instagram.com/globalcoollight',
            working_hours='Monday - Friday: 8:00 AM - 6:00 PM, Saturday: 9:00 AM - 4:00 PM, Sunday: Emergency calls only',
        )
        print(f"✅ Site settings created")

def create_service_categories():
    """Create realistic HVAC service categories"""
    categories_data = [
        {
            'name': 'Air Conditioning',
            'slug': 'air-conditioning',
            'description': 'Complete air conditioning solutions including installation, maintenance, and repair services for homes and businesses.',
            'icon': 'fas fa-snowflake'
        },
        {
            'name': 'Heating Systems',
            'slug': 'heating-systems', 
            'description': 'Professional heating system installation and maintenance for optimal comfort during cooler months.',
            'icon': 'fas fa-fire'
        },
        {
            'name': 'Ventilation',
            'slug': 'ventilation',
            'description': 'Indoor air quality solutions and ventilation systems for healthy living and working environments.',
            'icon': 'fas fa-wind'
        },
        {
            'name': 'Commercial HVAC',
            'slug': 'commercial-hvac',
            'description': 'Specialized HVAC solutions for offices, retail spaces, restaurants, and industrial facilities.',
            'icon': 'fas fa-building'
        },
        {
            'name': 'Emergency Services',
            'slug': 'emergency-services',
            'description': '24/7 emergency HVAC repair services for urgent heating and cooling issues.',
            'icon': 'fas fa-exclamation-triangle'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = ServiceCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categories.append(category)
        print(f"✅ Category: {category.name} {'created' if created else 'exists'}")
    
    return categories

def create_hvac_services(categories):
    """Create realistic HVAC services"""
    services_data = [
        # Air Conditioning Services
        {
            'category': 'air-conditioning',
            'name': 'Split AC Installation',
            'slug': 'split-ac-installation',
            'summary': 'Professional split air conditioner installation with warranty',
            'description': '''Complete split AC installation service including:
• Site assessment and load calculation
• Professional installation by certified technicians  
• Electrical connections and safety checks
• System testing and commissioning
• 2-year warranty on installation
• Free maintenance visit after 3 months

Perfect for homes, offices, and small commercial spaces. We work with leading brands including LG, Samsung, Daikin, and Mitsubishi.''',
            'base_price_min': 35000,
            'base_price_max': 85000,
            'duration_estimate': '4-8',
            'features': '''Professional installation by certified technicians
2-year warranty on installation work
Free 3-month maintenance check
Load calculation and sizing consultation
Electrical safety compliance
System performance testing'''
        },
        {
            'category': 'air-conditioning',
            'name': 'Central AC Installation',
            'slug': 'central-ac-installation', 
            'summary': 'Complete central air conditioning system installation for large spaces',
            'description': '''Comprehensive central AC installation including:
• Detailed load calculation and system design
• Ductwork installation and optimization
• Professional equipment installation
• Electrical connections and controls
• System balancing and testing
• 3-year warranty on installation

Ideal for large homes, offices, and commercial buildings. Energy-efficient solutions with smart controls available.''',
            'base_price_min': 150000,
            'base_price_max': 500000,
            'duration_estimate': '2-3-days',
            'features': '''Custom system design and load calculation
Professional ductwork installation
3-year comprehensive warranty
Energy-efficient equipment options
Smart thermostat integration
System balancing and optimization'''
        },
        {
            'category': 'air-conditioning',
            'name': 'AC Repair & Maintenance',
            'slug': 'ac-repair-maintenance',
            'summary': 'Expert AC repair and preventive maintenance services',
            'description': '''Professional AC repair and maintenance including:
• Comprehensive system diagnosis
• Refrigerant leak detection and repair
• Compressor and electrical repairs
• Filter replacement and cleaning
• Performance optimization
• Preventive maintenance plans available

Same-day service available for most repairs. All work backed by our satisfaction guarantee.''',
            'base_price_min': 3500,
            'base_price_max': 25000,
            'duration_estimate': '2-4',
            'features': '''Same-day service available
Comprehensive system diagnosis
Genuine parts and refrigerants
90-day warranty on repairs
Preventive maintenance plans
Emergency service available'''
        },
        
        # Heating Systems
        {
            'category': 'heating-systems',
            'name': 'Heat Pump Installation',
            'slug': 'heat-pump-installation',
            'summary': 'Energy-efficient heat pump systems for year-round comfort',
            'description': '''Professional heat pump installation service:
• Site evaluation and system sizing
• High-efficiency heat pump installation
• Electrical connections and controls
• System commissioning and testing
• Energy efficiency optimization
• 5-year manufacturer warranty

Ideal for Kenya's climate - provides both heating and cooling efficiently.''',
            'base_price_min': 120000,
            'base_price_max': 300000,
            'duration_estimate': '1-day',
            'features': '''Energy-efficient heating and cooling
Professional sizing and installation
5-year manufacturer warranty
Smart controls integration
Eco-friendly refrigerants
Annual maintenance included'''
        },
        
        # Ventilation Services  
        {
            'category': 'ventilation',
            'name': 'Exhaust Fan Installation',
            'slug': 'exhaust-fan-installation',
            'summary': 'Professional exhaust fan installation for kitchens and bathrooms',
            'description': '''Complete exhaust fan installation service:
• Proper sizing for your space
• Professional installation and ducting
• Electrical connections and switches
• Noise reduction optimization
• Weatherproofing and sealing
• 1-year installation warranty

Improve air quality and reduce humidity in kitchens, bathrooms, and utility rooms.''',
            'base_price_min': 8000,
            'base_price_max': 25000,
            'duration_estimate': '2-4',
            'features': '''Proper sizing consultation
Professional ducting installation
Noise reduction optimization
Weatherproof installation
1-year installation warranty
Energy-efficient models available'''
        },
        
        # Commercial HVAC
        {
            'category': 'commercial-hvac',
            'name': 'Office HVAC Systems',
            'slug': 'office-hvac-systems',
            'summary': 'Complete HVAC solutions for office buildings and commercial spaces',
            'description': '''Comprehensive commercial HVAC services:
• Load calculation and system design
• VRF/VRV system installation
• Ductwork and air distribution
• Building automation integration
• Energy management systems
• Ongoing maintenance contracts

Designed for optimal comfort and energy efficiency in commercial environments.''',
            'base_price_min': 500000,
            'base_price_max': 2000000,
            'duration_estimate': '1-week',
            'features': '''Custom commercial system design
Energy-efficient VRF/VRV systems
Building automation integration
Comprehensive maintenance contracts
Energy management and monitoring
24/7 emergency support available'''
        },
        
        # Emergency Services
        {
            'category': 'emergency-services',
            'name': '24/7 Emergency HVAC Repair',
            'slug': 'emergency-hvac-repair',
            'summary': 'Urgent HVAC repair services available 24/7',
            'description': '''Emergency HVAC repair service:
• 24/7 availability including weekends
• Rapid response within 2 hours
• Emergency diagnostic and repair
• Temporary solutions when needed
• Priority parts sourcing
• Emergency service guarantee

When your HVAC system fails, we're here to help restore your comfort quickly.''',
            'base_price_min': 5000,
            'base_price_max': 50000,
            'duration_estimate': '2-4',
            'features': '''24/7 emergency availability
Rapid 2-hour response time
Emergency diagnostic service
Temporary solutions provided
Priority parts sourcing
Weekend and holiday service'''
        }
    ]
    
    # Create services
    category_map = {cat.slug: cat for cat in categories}
    services = []
    
    for service_data in services_data:
        category = category_map[service_data.pop('category')]
        service_data['category'] = category
        service_data['is_active'] = True
        
        service, created = Service.objects.get_or_create(
            slug=service_data['slug'],
            defaults=service_data
        )
        services.append(service)
        print(f"✅ Service: {service.name} {'created' if created else 'exists'}")
    
    return services

def create_sample_clients():
    """Create realistic sample clients"""
    clients_data = [
        {
            'name': 'Sarah Wanjiku',
            'email': 'sarah.wanjiku@gmail.com',
            'phone': '+254 712 345 678',
            'client_type': 'individual',
            'address': 'Kileleshwa, Nairobi',
            'city': 'Nairobi',
            'county': 'Nairobi'
        },
        {
            'name': 'David Kimani',
            'email': 'david.kimani@yahoo.com', 
            'phone': '+254 723 456 789',
            'client_type': 'individual',
            'address': 'Karen, Nairobi',
            'city': 'Nairobi',
            'county': 'Nairobi'
        },
        {
            'name': 'TechHub Kenya Ltd',
            'email': 'facilities@techhub.co.ke',
            'phone': '+254 734 567 890',
            'client_type': 'business',
            'company_name': 'TechHub Kenya Ltd',
            'industry': 'Technology',
            'address': 'Westlands, Nairobi',
            'city': 'Nairobi', 
            'county': 'Nairobi'
        },
        {
            'name': 'Grace Muthoni',
            'email': 'grace.muthoni@outlook.com',
            'phone': '+254 745 678 901',
            'client_type': 'individual',
            'address': 'Runda, Nairobi',
            'city': 'Nairobi',
            'county': 'Nairobi'
        },
        {
            'name': 'Savannah Restaurant',
            'email': 'manager@savannahrestaurant.co.ke',
            'phone': '+254 756 789 012',
            'client_type': 'business',
            'company_name': 'Savannah Restaurant',
            'industry': 'Hospitality',
            'address': 'Kilimani, Nairobi',
            'city': 'Nairobi',
            'county': 'Nairobi'
        }
    ]
    
    clients = []
    for client_data in clients_data:
        client, created = Client.objects.get_or_create(
            email=client_data['email'],
            defaults=client_data
        )
        clients.append(client)
        print(f"✅ Client: {client.name} {'created' if created else 'exists'}")
    
    return clients

def create_admin_users():
    """Create admin users for the system"""
    # Create superuser
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@globalcool-light.com',
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        # Update the profile
        if hasattr(admin_user, 'profile'):
            admin_user.profile.employee_id = 'ADMIN001'
            admin_user.profile.role = 'admin'
            admin_user.profile.save()
        print(f"✅ Admin user created: admin/admin123")
    else:
        print(f"✅ Admin user exists: admin")
    
    # Create technicians
    technicians_data = [
        {
            'username': 'john_tech',
            'email': 'john@globalcool-light.com',
            'first_name': 'John',
            'last_name': 'Mwangi',
            'password': 'tech123',
            'employee_id': 'EMP001'
        },
        {
            'username': 'mary_tech',
            'email': 'mary@globalcool-light.com',
            'first_name': 'Mary',
            'last_name': 'Njeri',
            'password': 'tech123',
            'employee_id': 'EMP002'
        }
    ]

    technicians = []
    for tech_data in technicians_data:
        password = tech_data.pop('password')
        employee_id = tech_data.pop('employee_id')

        user, created = User.objects.get_or_create(
            username=tech_data['username'],
            defaults={**tech_data, 'is_staff': True}
        )
        if created:
            user.set_password(password)
            user.save()
            # Update the profile with employee_id
            if hasattr(user, 'profile'):
                user.profile.employee_id = employee_id
                user.profile.role = 'technician'
                user.profile.save()
            print(f"✅ Technician created: {user.username}/{password}")
        else:
            print(f"✅ Technician exists: {user.username}")
        technicians.append(user)
    
    return admin_user, technicians

def create_sample_bookings(services, clients, technicians):
    """Create realistic sample bookings"""
    from datetime import datetime
    import random
    
    bookings_data = [
        {
            'service': services[0],  # Split AC Installation
            'client': clients[0],    # Sarah Wanjiku
            'contact_name': 'Sarah Wanjiku',
            'contact_email': 'sarah.wanjiku@gmail.com',
            'contact_phone': '+254 712 345 678',
            'preferred_date': date.today() + timedelta(days=3),
            'preferred_time_slot': '08:00-10:00',
            'location_address': 'House No. 45, Kileleshwa Drive, Nairobi',
            'message': 'Need split AC installation in master bedroom. House is easily accessible.',
            'status': 'confirmed',
            'priority': 'normal',
            'source': 'website',
            'assigned_technician': technicians[0],
            'estimated_cost': Decimal('45000.00'),
            'admin_notes': 'Customer confirmed installation date. Site visit completed.'
        },
        {
            'service': services[2],  # AC Repair & Maintenance
            'client': clients[1],    # David Kimani
            'contact_name': 'David Kimani',
            'contact_email': 'david.kimani@yahoo.com',
            'contact_phone': '+254 723 456 789',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time_slot': '14:00-16:00',
            'location_address': 'Karen Estate, Plot 12, Nairobi',
            'message': 'AC not cooling properly. Urgent repair needed.',
            'status': 'in_progress',
            'priority': 'high',
            'source': 'phone',
            'assigned_technician': technicians[1],
            'estimated_cost': Decimal('8500.00'),
            'admin_notes': 'Technician on site. Compressor issue identified.'
        },
        {
            'service': services[5],  # Office HVAC Systems
            'client': clients[2],    # TechHub Kenya Ltd
            'contact_name': 'TechHub Facilities Manager',
            'contact_email': 'facilities@techhub.co.ke',
            'contact_phone': '+254 734 567 890',
            'preferred_date': date.today() + timedelta(days=14),
            'preferred_time_slot': '08:00-10:00',
            'location_address': 'TechHub Building, Westlands Square, Nairobi',
            'message': 'Complete HVAC system for new 3-floor office building. Need site assessment.',
            'status': 'new',
            'priority': 'normal',
            'source': 'email',
            'estimated_cost': Decimal('750000.00'),
            'admin_notes': 'Large commercial project. Site visit scheduled.'
        },
        {
            'service': services[6],  # Emergency HVAC Repair
            'client': clients[4],    # Savannah Restaurant
            'contact_name': 'Restaurant Manager',
            'contact_email': 'manager@savannahrestaurant.co.ke',
            'contact_phone': '+254 756 789 012',
            'preferred_date': date.today() - timedelta(days=2),
            'preferred_time_slot': '16:00-18:00',
            'location_address': 'Savannah Restaurant, Kilimani Plaza, Nairobi',
            'message': 'Kitchen exhaust system failed. Emergency repair needed immediately.',
            'status': 'completed',
            'priority': 'urgent',
            'source': 'phone',
            'assigned_technician': technicians[0],
            'estimated_cost': Decimal('15000.00'),
            'actual_cost': Decimal('12500.00'),
            'admin_notes': 'Emergency repair completed successfully. Customer satisfied.'
        },
        {
            'service': services[4],  # Exhaust Fan Installation
            'client': clients[3],    # Grace Muthoni
            'contact_name': 'Grace Muthoni',
            'contact_email': 'grace.muthoni@outlook.com',
            'contact_phone': '+254 745 678 901',
            'preferred_date': date.today() + timedelta(days=7),
            'preferred_time_slot': '10:00-12:00',
            'location_address': 'Runda Gardens, House 23, Nairobi',
            'message': 'Need exhaust fans installed in kitchen and two bathrooms.',
            'status': 'confirmed',
            'priority': 'normal',
            'source': 'website',
            'assigned_technician': technicians[1],
            'estimated_cost': Decimal('18000.00'),
            'admin_notes': 'Materials ordered. Installation scheduled.'
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
            print(f"✅ Booking created: {booking.contact_name} - {booking.service.name}")
        else:
            bookings.append(existing)
            print(f"✅ Booking exists: {existing.contact_name} - {existing.service.name}")
    
    return bookings

def create_sample_inquiries(services, clients):
    """Create sample inquiries"""
    inquiries_data = [
        {
            'service': services[1],  # Central AC Installation
            'contact_name': 'Peter Ochieng',
            'contact_email': 'peter.ochieng@gmail.com',
            'contact_phone': '+254 767 890 123',
            'subject': 'Central AC Quote for 4-bedroom house',
            'message': 'I need a quote for central AC installation in my 4-bedroom house in Lavington. The house is about 300 sqm.',
            'budget_range': 'KSh 200,000 - 300,000',
            'timeline': 'Within 2 months',
            'priority': 'normal',
            'status': 'new'
        },
        {
            'service': services[3],  # Heat Pump Installation
            'contact_name': 'Linda Akinyi',
            'contact_email': 'linda.akinyi@outlook.com',
            'contact_phone': '+254 778 901 234',
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
        print(f"✅ Inquiry: {inquiry.contact_name} - {inquiry.subject} {'created' if created else 'exists'}")
    
    return inquiries

def main():
    """Main function to populate all data"""
    print("🚀 Populating Global Cool-Light E.A LTD database with real data...")
    print("=" * 60)
    
    # Create company info
    create_company_info()
    
    # Create service categories and services
    categories = create_service_categories()
    services = create_hvac_services(categories)
    
    # Create users
    admin_user, technicians = create_admin_users()
    
    # Create clients
    clients = create_sample_clients()
    
    # Create bookings and inquiries
    bookings = create_sample_bookings(services, clients, technicians)
    inquiries = create_sample_inquiries(services, clients)
    
    print("=" * 60)
    print("✅ Database populated successfully!")
    print(f"📊 Summary:")
    print(f"   • {len(categories)} service categories")
    print(f"   • {len(services)} HVAC services")
    print(f"   • {len(clients)} sample clients")
    print(f"   • {len(bookings)} sample bookings")
    print(f"   • {len(inquiries)} sample inquiries")
    print(f"   • {len(technicians) + 1} users (1 admin + {len(technicians)} technicians)")
    print()
    print("🔐 Login credentials:")
    print("   Admin: admin / admin123")
    print("   Technician 1: john_tech / tech123")
    print("   Technician 2: mary_tech / tech123")
    print()
    print("🌐 Access URLs:")
    print("   Booking: http://127.0.0.1:8000/booking/")
    print("   Admin: http://127.0.0.1:8000/users/admin/dashboard/")

if __name__ == '__main__':
    main()
