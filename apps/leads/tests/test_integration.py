from django.test import TestCase, TransactionTestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.utils import timezone
from datetime import date, timedelta
from unittest.mock import patch

from apps.leads.models import Client, Booking, Inquiry
from apps.services.models import Service, ServiceCategory


class BookingFlowIntegrationTest(TransactionTestCase):
    """Integration test for complete booking flow"""
    
    def setUp(self):
        self.client = TestClient()
        
        # Create test data
        self.category = ServiceCategory.objects.create(
            name='HVAC Services',
            slug='hvac-services',
            description='Professional HVAC services'
        )
        self.service = Service.objects.create(
            name='AC Installation',
            slug='ac-installation',
            category=self.category,
            summary='Professional AC installation service',
            description='Complete AC installation with warranty',
            price_range='KSh 25,000 - 50,000',
            is_active=True
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@globalcool-light.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create technician
        self.technician = User.objects.create_user(
            username='technician',
            email='tech@globalcool-light.com',
            password='techpass123',
            is_staff=True,
            first_name='John',
            last_name='Tech'
        )
    
    def test_complete_booking_flow(self):
        """Test complete booking flow from creation to completion"""
        
        # Step 1: Customer creates booking
        booking_data = {
            'service': self.service.id,
            'contact_name': 'Alice Johnson',
            'contact_email': 'alice@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '123 Customer Street, Nairobi',
            'location_type': 'residential',
            'message': 'Need AC installation in master bedroom',
            'priority': 'normal'
        }
        
        # Clear any existing emails
        mail.outbox = []
        
        response = self.client.post(reverse('leads:booking_create'), booking_data)
        self.assertEqual(response.status_code, 302)  # Redirect to success
        
        # Check booking was created
        booking = Booking.objects.get(contact_email='alice@example.com')
        self.assertEqual(booking.status, 'new')
        self.assertEqual(booking.source, 'website')
        
        # Check confirmation email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Booking Confirmation', mail.outbox[0].subject)
        self.assertIn('alice@example.com', mail.outbox[0].to)
        
        # Step 2: Admin logs in and views booking
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.get(reverse('users:admin_bookings_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Johnson')
        
        # Step 3: Admin views booking details
        response = self.client.get(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Johnson')
        self.assertContains(response, 'AC Installation')
        
        # Step 4: Admin assigns technician
        mail.outbox = []  # Clear emails
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'assign_technician',
                'technician_id': self.technician.id
            }
        )
        self.assertEqual(response.status_code, 302)
        
        booking.refresh_from_db()
        self.assertEqual(booking.assigned_technician, self.technician)
        
        # Step 5: Admin confirms booking
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'update_status',
                'status': 'confirmed'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'confirmed')
        
        # Check status update email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Booking Confirmed', mail.outbox[0].subject)
        
        # Step 6: Admin starts work
        mail.outbox = []
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'update_status',
                'status': 'in_progress'
            }
        )
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'in_progress')
        
        # Step 7: Admin adds cost information
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'update_cost',
                'estimated_cost': '35000.00',
                'actual_cost': '32000.00'
            }
        )
        
        booking.refresh_from_db()
        self.assertEqual(float(booking.estimated_cost), 35000.00)
        self.assertEqual(float(booking.actual_cost), 32000.00)
        
        # Step 8: Admin completes booking
        mail.outbox = []
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'update_status',
                'status': 'completed'
            }
        )
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'completed')
        
        # Check completion email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Service Completed', mail.outbox[0].subject)
        
        # Step 9: Verify audit trail
        self.assertIn('Status changed from new to confirmed', booking.admin_notes)
        self.assertIn('Status changed from confirmed to in_progress', booking.admin_notes)
        self.assertIn('Status changed from in_progress to completed', booking.admin_notes)
    
    def test_booking_cancellation_flow(self):
        """Test booking cancellation flow"""
        
        # Create booking
        booking = Booking.objects.create(
            service=self.service,
            contact_name='Bob Smith',
            contact_email='bob@example.com',
            contact_phone='+254723456789',
            preferred_date=date.today() + timedelta(days=5),
            preferred_time_slot='afternoon',
            location_address='456 Test Avenue',
            location_type='commercial',
            priority='normal',
            source='website'
        )
        
        # Admin cancels booking
        self.client.login(username='admin', password='adminpass123')
        
        mail.outbox = []
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'update_status',
                'status': 'cancelled'
            }
        )
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
        
        # Check cancellation email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Booking Cancelled', mail.outbox[0].subject)
    
    def test_inquiry_to_booking_flow(self):
        """Test flow from inquiry to booking"""
        
        # Step 1: Customer submits inquiry
        inquiry_data = {
            'service': self.service.id,
            'contact_name': 'Carol Davis',
            'contact_email': 'carol@example.com',
            'contact_phone': '+254734567890',
            'subject': 'AC Installation Quote',
            'message': 'I need a quote for AC installation in my new office',
            'priority': 'normal'
        }
        
        response = self.client.post(reverse('leads:inquiry_create'), inquiry_data)
        self.assertEqual(response.status_code, 302)
        
        inquiry = Inquiry.objects.get(contact_email='carol@example.com')
        self.assertEqual(inquiry.status, 'new')
        
        # Step 2: Admin reviews inquiry and creates booking
        self.client.login(username='admin', password='adminpass123')
        
        # Create booking based on inquiry
        booking_data = {
            'service': self.service.id,
            'contact_name': inquiry.contact_name,
            'contact_email': inquiry.contact_email,
            'contact_phone': inquiry.contact_phone,
            'preferred_date': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '789 Office Building, Nairobi',
            'location_type': 'commercial',
            'message': 'Converted from inquiry',
            'priority': 'normal'
        }
        
        # Logout admin to simulate customer booking
        self.client.logout()
        
        response = self.client.post(reverse('leads:booking_create'), booking_data)
        self.assertEqual(response.status_code, 302)
        
        booking = Booking.objects.get(contact_email='carol@example.com')
        self.assertEqual(booking.contact_name, 'Carol Davis')
    
    def test_service_integration(self):
        """Test booking integration with services"""
        
        # Test booking from service detail page
        response = self.client.get(reverse('services:detail', kwargs={'slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Now')
        
        # Test service-specific booking form
        response = self.client.get(
            reverse('leads:booking_create_service', kwargs={'service_slug': self.service.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_service'], self.service)
        
        # Test booking creation with pre-selected service
        booking_data = {
            'service': self.service.id,
            'contact_name': 'David Wilson',
            'contact_email': 'david@example.com',
            'contact_phone': '+254745678901',
            'preferred_date': (date.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'evening',
            'location_address': '321 Service Street',
            'location_type': 'residential',
            'priority': 'normal'
        }
        
        response = self.client.post(
            reverse('leads:booking_create_service', kwargs={'service_slug': self.service.slug}),
            booking_data
        )
        self.assertEqual(response.status_code, 302)
        
        booking = Booking.objects.get(contact_email='david@example.com')
        self.assertEqual(booking.service, self.service)
    
    def test_admin_dashboard_analytics(self):
        """Test admin dashboard with booking analytics"""
        
        # Create multiple bookings with different statuses
        bookings_data = [
            {'status': 'new', 'count': 3},
            {'status': 'confirmed', 'count': 2},
            {'status': 'completed', 'count': 5},
            {'status': 'cancelled', 'count': 1}
        ]
        
        for data in bookings_data:
            for i in range(data['count']):
                booking = Booking.objects.create(
                    service=self.service,
                    contact_name=f'Customer {data["status"]} {i}',
                    contact_email=f'{data["status"]}{i}@example.com',
                    contact_phone=f'+25471234567{i}',
                    preferred_date=date.today() + timedelta(days=i+1),
                    preferred_time_slot='morning',
                    location_address=f'{i} Test Street',
                    location_type='residential',
                    priority='normal',
                    source='website',
                    status=data['status']
                )
                
                if data['status'] == 'completed':
                    booking.actual_cost = 30000 + (i * 1000)
                    booking.save()
        
        # Login as admin and check dashboard
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.get(reverse('users:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check analytics data is present
        self.assertIn('service_performance', response.context)
        self.assertIn('status_distribution', response.context)
        
        # Check specific metrics
        context = response.context
        self.assertEqual(context['total_bookings'], 11)  # 3+2+5+1
        self.assertEqual(context['completed_bookings'], 5)
        
        # Check revenue calculation
        expected_revenue = sum([30000 + (i * 1000) for i in range(5)])
        self.assertEqual(context['monthly_revenue'], expected_revenue)
    
    def test_error_handling(self):
        """Test error handling in booking flow"""
        
        # Test booking with non-existent service
        invalid_booking_data = {
            'service': 99999,  # Non-existent service
            'contact_name': 'Error Test',
            'contact_email': 'error@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '123 Error Street'
        }
        
        response = self.client.post(reverse('leads:booking_create'), invalid_booking_data)
        self.assertEqual(response.status_code, 200)  # Stay on form with errors
        self.assertFormError(response, 'form', 'service', 'Select a valid choice. That choice is not one of the available choices.')
        
        # Test admin access to non-existent booking
        self.client.login(username='admin', password='adminpass123')
        
        fake_uuid = '12345678-1234-1234-1234-123456789012'
        response = self.client.get(
            reverse('users:admin_booking_detail', kwargs={'booking_id': fake_uuid})
        )
        self.assertEqual(response.status_code, 404)
        
        # Test invalid status transition
        booking = Booking.objects.create(
            service=self.service,
            contact_name='Status Test',
            contact_email='status@example.com',
            contact_phone='+254712345678',
            preferred_date=date.today() + timedelta(days=7),
            preferred_time_slot='morning',
            location_address='123 Status Street',
            location_type='residential',
            priority='normal',
            source='website'
        )
        
        # Try invalid transition (new -> completed directly)
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': booking.booking_id}),
            {
                'action': 'update_status',
                'status': 'completed'
            }
        )
        
        # Should redirect but status shouldn't change
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'new')  # Status unchanged
