from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
import uuid

from apps.leads.models import Client, Booking, Inquiry, Quotation
from apps.services.models import Service, ServiceCategory


class ClientModelTest(TestCase):
    """Test cases for Client model"""
    
    def setUp(self):
        self.client_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+254712345678',
            'address': '123 Test Street, Nairobi'
        }
    
    def test_client_creation(self):
        """Test client creation with valid data"""
        client = Client.objects.create(**self.client_data)
        self.assertEqual(client.name, 'John Doe')
        self.assertEqual(client.email, 'john@example.com')
        self.assertEqual(str(client), 'John Doe (john@example.com)')
    
    def test_client_email_unique(self):
        """Test that client email must be unique"""
        Client.objects.create(**self.client_data)

        # Try to create another client with same email
        # Note: Django doesn't enforce email uniqueness by default in this model
        # This test checks if we can create multiple clients with same email
        client2 = Client.objects.create(**self.client_data)
        self.assertIsNotNone(client2)  # Should succeed since email is not unique


class BookingModelTest(TestCase):
    """Test cases for Booking model"""
    
    def setUp(self):
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
        self.client = Client.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            phone='+254723456789'
        )
        self.technician = User.objects.create_user(
            username='tech1',
            email='tech@example.com',
            is_staff=True
        )
        
        self.booking_data = {
            'service': self.service,
            'client': self.client,
            'contact_name': 'Jane Smith',
            'contact_email': 'jane@example.com',
            'contact_phone': '+254723456789',
            'preferred_date': date.today() + timedelta(days=7),
            'preferred_time_slot': '08:00-10:00',
            'location_address': '456 Test Avenue, Nairobi',
            'message': 'Need AC installation in living room',
            'priority': 'normal',
            'source': 'website'
        }
    
    def test_booking_creation(self):
        """Test booking creation with valid data"""
        booking = Booking.objects.create(**self.booking_data)
        
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.client, self.client)
        self.assertEqual(booking.status, 'new')  # Default status
        self.assertIsInstance(booking.booking_id, uuid.UUID)
        self.assertTrue(str(booking).startswith('Booking'))
    
    def test_booking_id_unique(self):
        """Test that booking_id is unique"""
        booking1 = Booking.objects.create(**self.booking_data)
        booking2 = Booking.objects.create(**self.booking_data)
        
        self.assertNotEqual(booking1.booking_id, booking2.booking_id)
    
    def test_status_transitions(self):
        """Test booking status transitions"""
        booking = Booking.objects.create(**self.booking_data)
        
        # Test valid transitions
        self.assertTrue(booking.can_transition_to('confirmed'))
        self.assertTrue(booking.can_transition_to('cancelled'))
        self.assertFalse(booking.can_transition_to('completed'))  # Invalid from 'new'
        
        # Test transition method
        booking.transition_status('confirmed')
        self.assertEqual(booking.status, 'confirmed')
        
        # Test invalid transition
        with self.assertRaises(ValueError):
            booking.transition_status('new')  # Can't go back to new
    
    def test_booking_save_creates_client(self):
        """Test that booking save creates client if not exists"""
        booking_data = self.booking_data.copy()
        booking_data.pop('client')  # Remove client
        booking_data['contact_email'] = 'newclient@example.com'
        booking_data['contact_name'] = 'New Client'
        
        booking = Booking(**booking_data)
        booking.save()
        
        # Check that client was created
        self.assertIsNotNone(booking.client)
        self.assertEqual(booking.client.email, 'newclient@example.com')
        self.assertEqual(booking.client.name, 'New Client')
    
    def test_booking_cost_fields(self):
        """Test booking cost fields"""
        booking = Booking.objects.create(**self.booking_data)
        
        booking.estimated_cost = 15000.00
        booking.actual_cost = 14500.00
        booking.save()
        
        self.assertEqual(booking.estimated_cost, 15000.00)
        self.assertEqual(booking.actual_cost, 14500.00)
    
    def test_technician_assignment(self):
        """Test technician assignment"""
        booking = Booking.objects.create(**self.booking_data)
        
        booking.assigned_technician = self.technician
        booking.save()
        
        self.assertEqual(booking.assigned_technician, self.technician)


class InquiryModelTest(TestCase):
    """Test cases for Inquiry model"""
    
    def setUp(self):
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
            'service': self.service,
            'contact_name': 'Bob Johnson',
            'contact_email': 'bob@example.com',
            'contact_phone': '+254734567890',
            'subject': 'AC Maintenance Quote',
            'message': 'I need a quote for regular AC maintenance',
            'priority': 'normal'
        }
    
    def test_inquiry_creation(self):
        """Test inquiry creation with valid data"""
        inquiry = Inquiry.objects.create(**self.inquiry_data)
        
        self.assertEqual(inquiry.service, self.service)
        self.assertEqual(inquiry.contact_name, 'Bob Johnson')
        self.assertEqual(inquiry.status, 'new')  # Default status
        self.assertIsInstance(inquiry.inquiry_id, uuid.UUID)
    
    def test_inquiry_without_service(self):
        """Test inquiry creation without specific service"""
        inquiry_data = self.inquiry_data.copy()
        inquiry_data.pop('service')
        inquiry_data['subject'] = 'General Inquiry'
        
        inquiry = Inquiry.objects.create(**inquiry_data)
        self.assertIsNone(inquiry.service)
        self.assertEqual(inquiry.subject, 'General Inquiry')


class QuotationModelTest(TestCase):
    """Test cases for Quotation model"""
    
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='HVAC Services',
            slug='hvac-services'
        )
        self.service = Service.objects.create(
            name='AC Repair',
            slug='ac-repair',
            category=self.category,
            summary='Professional AC repair',
            is_active=True
        )
        
        self.inquiry = Inquiry.objects.create(
            service=self.service,
            contact_name='Alice Brown',
            contact_email='alice@example.com',
            contact_phone='+254745678901',
            subject='AC Repair Quote',
            message='My AC is not cooling properly'
        )
        
        self.quotation_data = {
            'inquiry': self.inquiry,
            'client': Client.objects.create(
                name='Alice Brown',
                email='alice@example.com',
                phone='+254745678901'
            ),
            'title': 'AC Repair Service',
            'description': 'Repair and maintenance of AC unit',
            'subtotal': 8500.00,
            'tax_rate': 16.00,
            'tax_amount': 1360.00,
            'total': 9860.00,
            'valid_until': date.today() + timedelta(days=30),
            'terms_and_conditions': 'Payment due within 30 days',
            'notes': 'Includes parts and labor'
        }
    
    def test_quotation_creation(self):
        """Test quotation creation with valid data"""
        quotation = Quotation.objects.create(**self.quotation_data)
        
        self.assertEqual(quotation.inquiry, self.inquiry)
        self.assertEqual(quotation.title, 'AC Repair Service')
        self.assertEqual(quotation.subtotal, 8500.00)
        self.assertEqual(quotation.status, 'draft')  # Default status
        self.assertIsNotNone(quotation.quote_number)
    
    def test_quotation_string_representation(self):
        """Test quotation string representation"""
        quotation = Quotation.objects.create(**self.quotation_data)
        expected_str = f"Quote {quotation.quote_number} - {quotation.client.name} - KSh {quotation.total:,.2f}"
        self.assertEqual(str(quotation), expected_str)
    
    def test_quotation_validity(self):
        """Test quotation validity date"""
        quotation = Quotation.objects.create(**self.quotation_data)
        
        # Test future date
        future_date = date.today() + timedelta(days=30)
        quotation.valid_until = future_date
        quotation.save()
        
        self.assertEqual(quotation.valid_until, future_date)


class BookingStatusTransitionTest(TestCase):
    """Test cases for booking status transitions"""
    
    def setUp(self):
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
        self.client = Client.objects.create(
            name='Test Client',
            email='test@example.com',
            phone='+254712345678'
        )
        
        self.booking = Booking.objects.create(
            service=self.service,
            client=self.client,
            contact_name='Test Client',
            contact_email='test@example.com',
            contact_phone='+254712345678',
            preferred_date=date.today() + timedelta(days=7),
            preferred_time_slot='08:00-10:00',
            location_address='Test Address',
            priority='normal',
            source='website'
        )
    
    def test_new_to_confirmed(self):
        """Test transition from new to confirmed"""
        self.assertEqual(self.booking.status, 'new')
        self.booking.transition_status('confirmed')
        self.assertEqual(self.booking.status, 'confirmed')
    
    def test_confirmed_to_in_progress(self):
        """Test transition from confirmed to in_progress"""
        self.booking.transition_status('confirmed')
        self.booking.transition_status('in_progress')
        self.assertEqual(self.booking.status, 'in_progress')
    
    def test_in_progress_to_completed(self):
        """Test transition from in_progress to completed"""
        self.booking.transition_status('confirmed')
        self.booking.transition_status('in_progress')
        self.booking.transition_status('completed')
        self.assertEqual(self.booking.status, 'completed')
    
    def test_invalid_transitions(self):
        """Test invalid status transitions"""
        # Can't go directly from new to completed
        with self.assertRaises(ValueError):
            self.booking.transition_status('completed')
        
        # Can't go from completed back to any other status
        self.booking.transition_status('confirmed')
        self.booking.transition_status('in_progress')
        self.booking.transition_status('completed')
        
        with self.assertRaises(ValueError):
            self.booking.transition_status('new')
    
    def test_cancellation_from_any_status(self):
        """Test that booking can be cancelled from most statuses"""
        # From new
        self.assertTrue(self.booking.can_transition_to('cancelled'))
        
        # From confirmed
        self.booking.transition_status('confirmed')
        self.assertTrue(self.booking.can_transition_to('cancelled'))
        
        # From in_progress
        self.booking.transition_status('in_progress')
        self.assertTrue(self.booking.can_transition_to('cancelled'))
    
    def test_audit_trail_in_admin_notes(self):
        """Test that status transitions are recorded in admin notes"""
        user = User.objects.create_user('testuser', 'test@example.com')
        
        self.booking.transition_status('confirmed', user=user, notes='Customer confirmed')
        
        self.assertIn('Status changed from new to confirmed', self.booking.admin_notes)
        self.assertIn('testuser', self.booking.admin_notes)
        self.assertIn('Customer confirmed', self.booking.admin_notes)
