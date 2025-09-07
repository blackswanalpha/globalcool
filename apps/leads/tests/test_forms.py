from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta

from apps.leads.forms import BookingForm, InquiryForm, QuickBookingForm
from apps.services.models import Service, ServiceCategory


class BookingFormTest(TestCase):
    """Test cases for BookingForm"""
    
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
        
        self.valid_data = {
            'service': self.service.id,
            'contact_name': 'John Doe',
            'contact_email': 'john@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '123 Test Street, Nairobi',
            'location_type': 'residential',
            'message': 'Need AC installation in living room',
            'special_requirements': 'Please call before arriving',
            'priority': 'normal'
        }
    
    def test_booking_form_valid_data(self):
        """Test booking form with valid data"""
        form = BookingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_booking_form_required_fields(self):
        """Test booking form required fields validation"""
        form = BookingForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = [
            'service', 'contact_name', 'contact_email', 'contact_phone',
            'preferred_date', 'preferred_time_slot', 'location_address'
        ]
        
        for field in required_fields:
            self.assertIn(field, form.errors)
    
    def test_booking_form_email_validation(self):
        """Test email field validation"""
        invalid_data = self.valid_data.copy()
        invalid_data['contact_email'] = 'invalid-email'
        
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contact_email', form.errors)
    
    def test_booking_form_phone_validation(self):
        """Test phone number validation"""
        # Test invalid phone format
        invalid_data = self.valid_data.copy()
        invalid_data['contact_phone'] = '123456789'  # Invalid format
        
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contact_phone', form.errors)
        
        # Test valid Kenyan phone format
        valid_data = self.valid_data.copy()
        valid_data['contact_phone'] = '+254712345678'
        
        form = BookingForm(data=valid_data)
        self.assertTrue(form.is_valid())
    
    def test_booking_form_date_validation(self):
        """Test preferred date validation"""
        # Test past date
        invalid_data = self.valid_data.copy()
        invalid_data['preferred_date'] = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('preferred_date', form.errors)
        
        # Test far future date (more than 90 days)
        invalid_data['preferred_date'] = (date.today() + timedelta(days=100)).strftime('%Y-%m-%d')
        
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('preferred_date', form.errors)
    
    def test_booking_form_service_validation(self):
        """Test service field validation"""
        # Test inactive service
        inactive_service = Service.objects.create(
            name='Inactive Service',
            slug='inactive-service',
            category=self.category,
            summary='Inactive service',
            is_active=False
        )
        
        invalid_data = self.valid_data.copy()
        invalid_data['service'] = inactive_service.id
        
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('service', form.errors)
    
    def test_booking_form_save(self):
        """Test booking form save method"""
        form = BookingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        booking = form.save()
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.contact_name, 'John Doe')
        self.assertEqual(booking.contact_email, 'john@example.com')
        self.assertEqual(booking.status, 'new')  # Default status


class InquiryFormTest(TestCase):
    """Test cases for InquiryForm"""
    
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
        
        self.valid_data = {
            'service': self.service.id,
            'contact_name': 'Jane Smith',
            'contact_email': 'jane@example.com',
            'contact_phone': '+254723456789',
            'subject': 'AC Maintenance Quote',
            'message': 'I need a quote for regular AC maintenance for my office building',
            'priority': 'normal'
        }
    
    def test_inquiry_form_valid_data(self):
        """Test inquiry form with valid data"""
        form = InquiryForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_inquiry_form_required_fields(self):
        """Test inquiry form required fields validation"""
        form = InquiryForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = [
            'contact_name', 'contact_email', 'contact_phone', 'subject', 'message'
        ]
        
        for field in required_fields:
            self.assertIn(field, form.errors)
    
    def test_inquiry_form_optional_service(self):
        """Test that service field is optional in inquiry form"""
        data_without_service = self.valid_data.copy()
        data_without_service.pop('service')
        
        form = InquiryForm(data=data_without_service)
        self.assertTrue(form.is_valid())
    
    def test_inquiry_form_message_length(self):
        """Test message field length validation"""
        # Test very short message
        invalid_data = self.valid_data.copy()
        invalid_data['message'] = 'Hi'  # Too short
        
        form = InquiryForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
        
        # Test very long message
        invalid_data['message'] = 'A' * 2001  # Too long (assuming max 2000 chars)
        
        form = InquiryForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
    
    def test_inquiry_form_save(self):
        """Test inquiry form save method"""
        form = InquiryForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        inquiry = form.save()
        self.assertEqual(inquiry.service, self.service)
        self.assertEqual(inquiry.contact_name, 'Jane Smith')
        self.assertEqual(inquiry.subject, 'AC Maintenance Quote')
        self.assertEqual(inquiry.status, 'new')  # Default status


class QuickBookingFormTest(TestCase):
    """Test cases for QuickBookingForm"""
    
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='HVAC Services',
            slug='hvac-services'
        )
        self.service = Service.objects.create(
            name='Emergency Repair',
            slug='emergency-repair',
            category=self.category,
            summary='Emergency HVAC repair',
            is_active=True
        )
        
        self.valid_data = {
            'service': self.service.id,
            'contact_name': 'Bob Johnson',
            'contact_email': 'bob@example.com',
            'contact_phone': '+254734567890',
            'preferred_date': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'location_address': '456 Emergency Street, Nairobi',
            'message': 'AC stopped working, need urgent repair'
        }
    
    def test_quick_booking_form_valid_data(self):
        """Test quick booking form with valid data"""
        form = QuickBookingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_quick_booking_form_fewer_required_fields(self):
        """Test that quick booking form has fewer required fields"""
        minimal_data = {
            'service': self.service.id,
            'contact_name': 'Bob Johnson',
            'contact_email': 'bob@example.com',
            'contact_phone': '+254734567890',
            'location_address': '456 Emergency Street, Nairobi'
        }
        
        form = QuickBookingForm(data=minimal_data)
        self.assertTrue(form.is_valid())
    
    def test_quick_booking_form_defaults(self):
        """Test quick booking form default values"""
        form = QuickBookingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        booking = form.save()
        self.assertEqual(booking.priority, 'high')  # Default for quick booking
        self.assertEqual(booking.preferred_time_slot, 'any')  # Default time slot


class FormWidgetTest(TestCase):
    """Test form widgets and styling"""
    
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
    
    def test_booking_form_widgets(self):
        """Test that booking form has proper widgets"""
        form = BookingForm()
        
        # Check that date field has date widget
        self.assertEqual(form.fields['preferred_date'].widget.input_type, 'date')
        
        # Check that message field is textarea
        self.assertEqual(form.fields['message'].widget.__class__.__name__, 'Textarea')
        
        # Check that service field has proper queryset (only active services)
        service_choices = [choice[0] for choice in form.fields['service'].choices if choice[0]]
        self.assertIn(self.service.id, service_choices)
    
    def test_form_css_classes(self):
        """Test that forms have proper CSS classes"""
        form = BookingForm()
        
        # Check that fields have form-control class
        for field_name, field in form.fields.items():
            if hasattr(field.widget, 'attrs'):
                self.assertIn('form-control', field.widget.attrs.get('class', ''))
    
    def test_form_placeholders(self):
        """Test that forms have helpful placeholders"""
        form = BookingForm()
        
        # Check specific placeholders
        self.assertIn('placeholder', form.fields['contact_name'].widget.attrs)
        self.assertIn('placeholder', form.fields['contact_email'].widget.attrs)
        self.assertIn('placeholder', form.fields['contact_phone'].widget.attrs)


class FormValidationEdgeCasesTest(TestCase):
    """Test edge cases in form validation"""
    
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
    
    def test_booking_form_xss_protection(self):
        """Test that forms protect against XSS attacks"""
        malicious_data = {
            'service': self.service.id,
            'contact_name': '<script>alert("xss")</script>John Doe',
            'contact_email': 'john@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '123 Test Street',
            'message': '<script>alert("xss")</script>Test message'
        }
        
        form = BookingForm(data=malicious_data)
        if form.is_valid():
            booking = form.save()
            # Check that script tags are not executed (they should be escaped)
            self.assertNotIn('<script>', booking.contact_name)
            self.assertNotIn('<script>', booking.message)
    
    def test_booking_form_sql_injection_protection(self):
        """Test that forms protect against SQL injection"""
        malicious_data = {
            'service': self.service.id,
            'contact_name': "'; DROP TABLE bookings; --",
            'contact_email': 'john@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': '123 Test Street'
        }
        
        form = BookingForm(data=malicious_data)
        # Form should still be valid (Django ORM protects against SQL injection)
        self.assertTrue(form.is_valid())
        
        # Should be able to save without issues
        booking = form.save()
        self.assertEqual(booking.contact_name, "'; DROP TABLE bookings; --")
    
    def test_unicode_handling(self):
        """Test that forms handle Unicode characters properly"""
        unicode_data = {
            'service': self.service.id,
            'contact_name': 'José María González',
            'contact_email': 'jose@example.com',
            'contact_phone': '+254712345678',
            'preferred_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'preferred_time_slot': 'morning',
            'location_address': 'Calle de la Constitución, Madrid',
            'message': 'Necesito instalación de aire acondicionado'
        }
        
        form = BookingForm(data=unicode_data)
        self.assertTrue(form.is_valid())
        
        booking = form.save()
        self.assertEqual(booking.contact_name, 'José María González')
        self.assertEqual(booking.message, 'Necesito instalación de aire acondicionado')
