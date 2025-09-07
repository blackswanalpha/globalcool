from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
import random

from apps.services.models import ServiceCategory, Service
from apps.portfolio.models import Project, ProjectImage, Testimonial
from apps.leads.models import Client, Booking, Inquiry, Quotation


class Command(BaseCommand):
    help = 'Populate the database with sample HVAC business data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for Global Cool-Light E.A LTD...')
        
        # Create service categories and services
        self.create_services()
        
        # Create clients
        self.create_clients()
        
        # Create bookings
        self.create_bookings()
        
        # Create inquiries and quotations
        self.create_inquiries_and_quotations()
        
        # Create portfolio projects
        self.create_portfolio()
        
        # Create testimonials
        self.create_testimonials()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )

    def create_services(self):
        """Create service categories and services"""
        categories_data = [
            {
                'name': 'Air Conditioning',
                'slug': 'air-conditioning',
                'description': 'Complete AC installation, maintenance, and repair services',
                'icon': 'fas fa-snowflake',
                'services': [
                    {
                        'name': 'AC Installation',
                        'summary': 'Professional installation of air conditioning systems for homes and businesses',
                        'description': 'Complete installation service including site assessment, system design, and professional installation with warranty.',
                        'base_price_min': 25000,
                        'base_price_max': 150000,
                        'duration_estimate': '4-8',
                        'features': 'Site assessment\nProfessional installation\n2-year warranty\nFree maintenance for 6 months'
                    },
                    {
                        'name': 'AC Repair',
                        'summary': 'Quick and reliable air conditioning repair services',
                        'description': 'Expert diagnosis and repair of all AC issues with genuine parts and experienced technicians.',
                        'base_price_min': 3000,
                        'base_price_max': 25000,
                        'duration_estimate': '2-4',
                        'features': 'Free diagnosis\nGenuine parts\nSame-day service\n90-day warranty on repairs'
                    },
                    {
                        'name': 'AC Maintenance',
                        'summary': 'Regular maintenance to keep your AC running efficiently',
                        'description': 'Comprehensive maintenance service to ensure optimal performance and extend system life.',
                        'base_price_min': 2500,
                        'base_price_max': 8000,
                        'duration_estimate': '1-2',
                        'features': 'Complete system cleaning\nFilter replacement\nPerformance optimization\nMaintenance report'
                    }
                ]
            },
            {
                'name': 'Cold Room Solutions',
                'slug': 'cold-room-solutions',
                'description': 'Commercial cold room installation and maintenance',
                'icon': 'fas fa-warehouse',
                'services': [
                    {
                        'name': 'Cold Room Installation',
                        'summary': 'Complete cold room setup for businesses',
                        'description': 'Professional cold room installation with insulation, refrigeration systems, and temperature controls.',
                        'base_price_min': 200000,
                        'base_price_max': 2000000,
                        'duration_estimate': '1-week',
                        'features': 'Custom design\nHigh-quality insulation\nDigital temperature control\n5-year warranty'
                    },
                    {
                        'name': 'Cold Room Maintenance',
                        'summary': 'Regular maintenance for cold storage systems',
                        'description': 'Preventive maintenance to ensure consistent temperatures and system reliability.',
                        'base_price_min': 15000,
                        'base_price_max': 50000,
                        'duration_estimate': '2-4',
                        'features': 'Temperature calibration\nSystem inspection\nPreventive repairs\nMaintenance schedule'
                    }
                ]
            },
            {
                'name': 'HVAC Systems',
                'slug': 'hvac-systems',
                'description': 'Complete heating, ventilation, and air conditioning solutions',
                'icon': 'fas fa-wind',
                'services': [
                    {
                        'name': 'HVAC Installation',
                        'summary': 'Complete HVAC system installation',
                        'description': 'Full HVAC system design and installation for optimal climate control.',
                        'base_price_min': 100000,
                        'base_price_max': 500000,
                        'duration_estimate': '2-3-days',
                        'features': 'System design\nProfessional installation\nEnergy efficiency optimization\n3-year warranty'
                    }
                ]
            }
        ]

        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': cat_data['slug'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                }
            )
            
            for service_data in cat_data['services']:
                Service.objects.get_or_create(
                    category=category,
                    name=service_data['name'],
                    defaults=service_data
                )

        self.stdout.write('✓ Created services and categories')

    def create_clients(self):
        """Create sample clients"""
        clients_data = [
            {
                'name': 'John Doe',
                'email': 'john.doe@email.com',
                'phone': '+254712345678',
                'client_type': 'individual',
                'address': 'Westlands, Nairobi',
                'city': 'Nairobi',
                'county': 'Nairobi'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@email.com',
                'phone': '+254723456789',
                'client_type': 'individual',
                'address': 'Karen, Nairobi',
                'city': 'Nairobi',
                'county': 'Nairobi'
            },
            {
                'name': 'Acme Corporation',
                'email': 'info@acmecorp.co.ke',
                'phone': '+254734567890',
                'client_type': 'business',
                'company_name': 'Acme Corporation',
                'industry': 'Manufacturing',
                'address': 'Industrial Area, Nairobi',
                'city': 'Nairobi',
                'county': 'Nairobi'
            },
            {
                'name': 'Sarah Wilson',
                'email': 'sarah.wilson@email.com',
                'phone': '+254745678901',
                'client_type': 'individual',
                'address': 'Kilimani, Nairobi',
                'city': 'Nairobi',
                'county': 'Nairobi'
            },
            {
                'name': 'Tech Solutions Ltd',
                'email': 'contact@techsolutions.co.ke',
                'phone': '+254756789012',
                'client_type': 'business',
                'company_name': 'Tech Solutions Ltd',
                'industry': 'Technology',
                'address': 'Upperhill, Nairobi',
                'city': 'Nairobi',
                'county': 'Nairobi'
            }
        ]

        for client_data in clients_data:
            Client.objects.get_or_create(
                email=client_data['email'],
                defaults=client_data
            )

        self.stdout.write('✓ Created sample clients')

    def create_bookings(self):
        """Create sample bookings"""
        services = list(Service.objects.all())
        clients = list(Client.objects.all())
        
        if not services or not clients:
            self.stdout.write('⚠ No services or clients found, skipping bookings')
            return

        # Create bookings for the last 30 days
        for i in range(25):
            booking_date = timezone.now().date() - timedelta(days=random.randint(0, 30))
            client = random.choice(clients)
            service = random.choice(services)
            
            status_choices = ['new', 'confirmed', 'in_progress', 'completed', 'cancelled']
            status = random.choice(status_choices)
            
            # More recent bookings are more likely to be new/confirmed
            if booking_date >= timezone.now().date() - timedelta(days=7):
                status = random.choice(['new', 'confirmed', 'in_progress'])
            
            Booking.objects.create(
                service=service,
                client=client,
                contact_name=client.name,
                contact_email=client.email,
                contact_phone=client.phone,
                preferred_date=booking_date,
                preferred_time_slot=random.choice(['08:00-10:00', '10:00-12:00', '14:00-16:00', 'flexible']),
                location_address=client.address or 'Nairobi, Kenya',
                status=status,
                priority=random.choice(['normal', 'normal', 'high', 'low']),  # More normal priority
                message=f'Need {service.name.lower()} service at my location.',
                estimated_cost=random.randint(int(service.base_price_min or 5000), int(service.base_price_max or 50000))
            )

        self.stdout.write('✓ Created sample bookings')

    def create_inquiries_and_quotations(self):
        """Create sample inquiries and quotations"""
        services = list(Service.objects.all())
        clients = list(Client.objects.all())
        
        if not services or not clients:
            return

        # Create inquiries
        for i in range(15):
            client = random.choice(clients)
            service = random.choice(services) if random.choice([True, False]) else None
            
            inquiry = Inquiry.objects.create(
                client=client,
                service=service,
                contact_name=client.name,
                contact_email=client.email,
                contact_phone=client.phone,
                subject=f'Inquiry about {service.name if service else "HVAC services"}',
                message=f'I would like to get more information about {service.name.lower() if service else "your services"}.',
                status=random.choice(['new', 'in_review', 'quoted', 'closed']),
                priority=random.choice(['normal', 'high', 'low'])
            )
            
            # Create quotation for some inquiries
            if random.choice([True, False]) and inquiry.status in ['quoted', 'closed']:
                subtotal = random.randint(10000, 200000)
                Quotation.objects.create(
                    inquiry=inquiry,
                    client=client,
                    title=f'Quotation for {service.name if service else "HVAC Services"}',
                    description=f'Professional {service.name.lower() if service else "HVAC"} service quotation',
                    subtotal=subtotal,
                    tax_rate=16.00,
                    tax_amount=(subtotal * 16) / 100,
                    total=subtotal + (subtotal * 16) / 100,
                    valid_until=timezone.now().date() + timedelta(days=30),
                    status=random.choice(['sent', 'viewed', 'accepted', 'rejected']),
                    items=[
                        {
                            'description': service.name if service else 'HVAC Service',
                            'quantity': 1,
                            'unit_price': subtotal,
                            'total': subtotal
                        }
                    ]
                )

        self.stdout.write('✓ Created sample inquiries and quotations')

    def create_portfolio(self):
        """Create sample portfolio projects"""
        services = list(Service.objects.all())
        
        projects_data = [
            {
                'title': 'Westgate Mall HVAC Installation',
                'summary': 'Complete HVAC system installation for major shopping mall',
                'description': 'Comprehensive HVAC installation project covering 50,000 sq ft of retail space with energy-efficient systems.',
                'client_name': 'Westgate Mall Management',
                'location': 'Westlands, Nairobi',
                'project_type': 'Commercial',
                'status': 'completed',
                'start_date': date(2024, 1, 15),
                'end_date': date(2024, 3, 20),
                'is_featured': True
            },
            {
                'title': 'Karen Hospital Cold Room Setup',
                'summary': 'Medical-grade cold storage installation',
                'description': 'Installation of temperature-controlled storage systems for pharmaceutical and medical supplies.',
                'client_name': 'Karen Hospital',
                'location': 'Karen, Nairobi',
                'project_type': 'Healthcare',
                'status': 'completed',
                'start_date': date(2023, 11, 10),
                'end_date': date(2023, 12, 5),
                'is_featured': True
            },
            {
                'title': 'Residential AC Installation - Kilimani',
                'summary': 'Multi-unit residential AC installation',
                'description': 'Installation of energy-efficient AC units in luxury residential complex.',
                'client_name': 'Kilimani Residences',
                'location': 'Kilimani, Nairobi',
                'project_type': 'Residential',
                'status': 'completed',
                'start_date': date(2024, 2, 1),
                'end_date': date(2024, 2, 15)
            }
        ]

        for project_data in projects_data:
            project = Project.objects.create(**project_data)
            
            # Add some services to the project
            if services:
                project.services.add(*random.sample(services, min(3, len(services))))

        self.stdout.write('✓ Created sample portfolio projects')

    def create_testimonials(self):
        """Create sample testimonials"""
        projects = list(Project.objects.all())
        
        testimonials_data = [
            {
                'author_name': 'David Ochieng',
                'author_title': 'Facilities Manager',
                'author_company': 'Westgate Mall',
                'quote': 'Global Cool-Light delivered exceptional HVAC installation services. Their team was professional, timely, and the system works perfectly. Highly recommended!',
                'rating': 5,
                'is_featured': True
            },
            {
                'author_name': 'Dr. Mary Wanjiku',
                'author_title': 'Chief Medical Officer',
                'author_company': 'Karen Hospital',
                'quote': 'The cold room installation was flawless. Temperature control is precise and reliable - exactly what we needed for our medical supplies.',
                'rating': 5,
                'is_featured': True
            },
            {
                'author_name': 'James Mwangi',
                'author_title': 'Property Owner',
                'quote': 'Excellent AC installation service. The technicians were knowledgeable and completed the work efficiently. Very satisfied with the results.',
                'rating': 4,
            }
        ]

        for i, testimonial_data in enumerate(testimonials_data):
            if projects and i < len(projects):
                testimonial_data['related_project'] = projects[i]
            
            Testimonial.objects.create(**testimonial_data)

        self.stdout.write('✓ Created sample testimonials')
