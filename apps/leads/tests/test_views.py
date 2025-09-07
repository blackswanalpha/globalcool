from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from unittest.mock import patch

from apps.leads.models import Client, Booking, Inquiry
from apps.services.models import Service, ServiceCategory
from apps.leads.forms import BookingForm, InquiryForm


class BookingViewsTest(TestCase):
    """Test cases for booking views"""
    
    def setUp(self):
        self.client = TestClient()
        
        # Create test data
        self.category = ServiceCategory.objects.create(
            name='HVAC Services',
            slug='hvac-services'
        )
        self.service = Service.objects.create(
            name='AC Installation',
            slug='ac-installation',
            category=self.category,
            summary='Professional AC installation',
            is_active=True
        )
        
        self.booking_data = {
            'service': self.service.id,
            'contact_name': 'John Doe',
            'contact_email': 'john@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '123 Test Street, Nairobi',
            'location_type': 'residential',
            'message': 'Need AC installation',
            'priority': 'normal'
        }
    
    def test_booking_create_view_get(self):
        """Test GET request to booking create view"""
        response = self.client.get(reverse('leads:booking_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book a Service')
        self.assertIsInstance(response.context['form'], BookingForm)
    
    def test_booking_create_view_with_service_slug(self):
        """Test booking create view with pre-selected service"""
        response = self.client.get(
            reverse('leads:booking_create_service', kwargs={'service_slug': self.service.slug})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_service'], self.service)
    
    @patch('apps.leads.views.send_mail')
    def test_booking_create_view_post_valid(self, mock_send_mail):
        """Test POST request with valid booking data"""
        mock_send_mail.return_value = True
        
        response = self.client.post(reverse('leads:booking_create'), self.booking_data)
        
        # Should redirect to success page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('leads:booking_success'))
        
        # Check booking was created
        booking = Booking.objects.get(contact_email='john@example.com')
        self.assertEqual(booking.contact_name, 'John Doe')
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.status, 'new')
        self.assertEqual(booking.source, 'website')
        
        # Check email was sent
        mock_send_mail.assert_called_once()
    
    def test_booking_create_view_post_invalid(self):
        """Test POST request with invalid booking data"""
        invalid_data = self.booking_data.copy()
        invalid_data['contact_email'] = 'invalid-email'  # Invalid email
        invalid_data['preferred_date'] = '2020-01-01'  # Past date
        
        response = self.client.post(reverse('leads:booking_create'), invalid_data)
        
        # Should stay on same page with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'contact_email', 'Enter a valid email address.')
        
        # No booking should be created
        self.assertEqual(Booking.objects.count(), 0)
    
    def test_booking_success_view(self):
        """Test booking success view"""
        # Create a booking first
        booking = Booking.objects.create(
            service=self.service,
            contact_name='John Doe',
            contact_email='john@example.com',
            contact_phone='+254712345678',
            preferred_date=date.today() + timedelta(days=7),
            preferred_time_slot='morning',
            location_address='123 Test Street',
            location_type='residential',
            priority='normal',
            source='website'
        )
        
        # Set booking ID in session
        session = self.client.session
        session['booking_id'] = str(booking.booking_id)
        session.save()
        
        response = self.client.get(reverse('leads:booking_success'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking'], booking)
        self.assertContains(response, 'Booking Confirmed')
    
    def test_booking_success_view_no_session(self):
        """Test booking success view without booking ID in session"""
        response = self.client.get(reverse('leads:booking_success'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('booking'))


class InquiryViewsTest(TestCase):
    """Test cases for inquiry views"""
    
    def setUp(self):
        self.client = TestClient()
        
        self.category = ServiceCategory.objects.create(
            name='HVAC Services',
            slug='hvac-services'
        )
        self.service = Service.objects.create(
            name='AC Maintenance',
            slug='ac-maintenance',
            category=self.category,
            summary='Regular AC maintenance',
            is_active=True
        )
        
        self.inquiry_data = {
            'service': self.service.id,
            'contact_name': 'Jane Smith',
            'contact_email': 'jane@example.com',
            'contact_phone': '+254723456789',
            'subject': 'AC Maintenance Quote',
            'message': 'I need a quote for regular AC maintenance',
            'priority': 'normal'
        }
    
    def test_inquiry_create_view_get(self):
        """Test GET request to inquiry create view"""
        response = self.client.get(reverse('leads:inquiry_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Request a Quote')
        self.assertIsInstance(response.context['form'], InquiryForm)
    
    @patch('apps.leads.views.send_mail')
    def test_inquiry_create_view_post_valid(self, mock_send_mail):
        """Test POST request with valid inquiry data"""
        mock_send_mail.return_value = True
        
        response = self.client.post(reverse('leads:inquiry_create'), self.inquiry_data)
        
        # Should redirect to success page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('leads:inquiry_success'))
        
        # Check inquiry was created
        inquiry = Inquiry.objects.get(contact_email='jane@example.com')
        self.assertEqual(inquiry.contact_name, 'Jane Smith')
        self.assertEqual(inquiry.service, self.service)
        self.assertEqual(inquiry.status, 'new')
    
    def test_inquiry_success_view(self):
        """Test inquiry success view"""
        # Create an inquiry first
        inquiry = Inquiry.objects.create(
            service=self.service,
            contact_name='Jane Smith',
            contact_email='jane@example.com',
            contact_phone='+254723456789',
            subject='AC Maintenance Quote',
            message='I need a quote for regular AC maintenance',
            priority='normal'
        )
        
        # Set inquiry ID in session
        session = self.client.session
        session['inquiry_id'] = str(inquiry.inquiry_id)
        session.save()
        
        response = self.client.get(reverse('leads:inquiry_success'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['inquiry'], inquiry)
        self.assertContains(response, 'Inquiry Submitted')


class AdminBookingViewsTest(TestCase):
    """Test cases for admin booking views"""
    
    def setUp(self):
        self.client = TestClient()
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123'
        )
        
        # Create test data
        self.category = ServiceCategory.objects.create(
            name='HVAC Services',
            slug='hvac-services'
        )
        self.service = Service.objects.create(
            name='AC Installation',
            slug='ac-installation',
            category=self.category,
            summary='Professional AC installation',
            is_active=True
        )
        
        self.booking = Booking.objects.create(
            service=self.service,
            contact_name='Test Customer',
            contact_email='customer@example.com',
            contact_phone='+254712345678',
            preferred_date=date.today() + timedelta(days=7),
            preferred_time_slot='morning',
            location_address='Test Address',
            location_type='residential',
            priority='normal',
            source='website'
        )
    
    def test_admin_bookings_list_requires_login(self):
        """Test that admin bookings list requires login"""
        response = self.client.get(reverse('users:admin_bookings_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_admin_bookings_list_requires_staff(self):
        """Test that admin bookings list requires staff permission"""
        self.client.login(username='user', password='testpass123')
        response = self.client.get(reverse('users:admin_bookings_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_admin_bookings_list_success(self):
        """Test successful access to admin bookings list"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('users:admin_bookings_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Booking Management')
        self.assertIn('bookings', response.context)
        self.assertIn(self.booking, response.context['bookings'])
    
    def test_admin_bookings_list_filtering(self):
        """Test filtering in admin bookings list"""
        self.client.login(username='admin', password='testpass123')
        
        # Test status filter
        response = self.client.get(reverse('users:admin_bookings_list'), {'status': 'new'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.booking, response.context['bookings'])
        
        # Test search
        response = self.client.get(reverse('users:admin_bookings_list'), {'search': 'Test Customer'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.booking, response.context['bookings'])
    
    def test_admin_booking_detail_success(self):
        """Test successful access to admin booking detail"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(
            reverse('users:admin_booking_detail', kwargs={'booking_id': self.booking.booking_id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking'], self.booking)
        self.assertContains(response, 'Booking Details')
    
    def test_admin_booking_status_update(self):
        """Test booking status update via admin interface"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': self.booking.booking_id}),
            {
                'action': 'update_status',
                'status': 'confirmed'
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Check booking was updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'confirmed')
    
    def test_admin_booking_technician_assignment(self):
        """Test technician assignment via admin interface"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': self.booking.booking_id}),
            {
                'action': 'assign_technician',
                'technician_id': self.admin_user.id
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Check technician was assigned
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.assigned_technician, self.admin_user)
    
    def test_admin_booking_cost_update(self):
        """Test cost update via admin interface"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': self.booking.booking_id}),
            {
                'action': 'update_cost',
                'estimated_cost': '15000.00',
                'actual_cost': '14500.00'
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Check costs were updated
        self.booking.refresh_from_db()
        self.assertEqual(float(self.booking.estimated_cost), 15000.00)
        self.assertEqual(float(self.booking.actual_cost), 14500.00)
    
    def test_admin_booking_notes_update(self):
        """Test admin notes update via admin interface"""
        self.client.login(username='admin', password='testpass123')
        
        response = self.client.post(
            reverse('users:admin_booking_detail', kwargs={'booking_id': self.booking.booking_id}),
            {
                'action': 'update_notes',
                'admin_notes': 'Customer called to confirm appointment'
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Check notes were updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.admin_notes, 'Customer called to confirm appointment')
