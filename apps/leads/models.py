from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
import uuid


class Client(models.Model):
    """Customer/Client information"""
    CLIENT_TYPES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('government', 'Government'),
        ('ngo', 'NGO'),
    ]

    CONTACT_METHODS = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]

    # Basic information
    name = models.CharField(max_length=200, help_text="Full name or company name")
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPES, default='individual')

    # Contact information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    email = models.EmailField()
    phone = models.CharField(validators=[phone_regex], max_length=17)
    alternative_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)

    # Business details (if applicable)
    company_name = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)

    # Notes and preferences
    notes = models.TextField(blank=True, help_text="Internal notes about the client")
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHODS,
        default='phone'
    )

    # Tracking
    total_bookings = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"


class Booking(models.Model):
    """Service booking requests"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    TIME_SLOTS = [
        ('08:00-10:00', '8:00 AM - 10:00 AM'),
        ('10:00-12:00', '10:00 AM - 12:00 PM'),
        ('12:00-14:00', '12:00 PM - 2:00 PM'),
        ('14:00-16:00', '2:00 PM - 4:00 PM'),
        ('16:00-18:00', '4:00 PM - 6:00 PM'),
        ('flexible', 'Flexible'),
    ]

    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('phone', 'Phone Call'),
        ('email', 'Email'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('walk_in', 'Walk-in'),
    ]

    # Basic information
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='bookings')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)

    # Contact details (for walk-in bookings without client record)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=17)

    # Booking details
    preferred_date = models.DateField()
    preferred_time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default='flexible')
    actual_date = models.DateField(null=True, blank=True)
    actual_time = models.TimeField(null=True, blank=True)

    # Additional information
    message = models.TextField(blank=True, help_text="Special requirements or notes")
    location_address = models.TextField(help_text="Service location address")

    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')

    # Admin fields
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for staff")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_id.hex[:8]} - {self.contact_name} - {self.service.name}"

    def save(self, *args, **kwargs):
        # Create or link client
        if not self.client and self.contact_email:
            client, created = Client.objects.get_or_create(
                email=self.contact_email,
                defaults={
                    'name': self.contact_name,
                    'phone': self.contact_phone,
                }
            )
            self.client = client
        super().save(*args, **kwargs)

    def can_transition_to(self, new_status):
        """Check if booking can transition to new status"""
        valid_transitions = {
            'new': ['confirmed', 'cancelled'],
            'confirmed': ['in_progress', 'cancelled', 'rescheduled'],
            'in_progress': ['completed', 'cancelled'],
            'completed': [],  # Final state
            'cancelled': [],  # Final state
            'rescheduled': ['confirmed', 'cancelled'],
        }
        return new_status in valid_transitions.get(self.status, [])

    def transition_status(self, new_status, user=None, notes=None):
        """Safely transition booking status with validation"""
        if not self.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")

        old_status = self.status
        self.status = new_status

        # Add audit trail note
        if notes:
            audit_note = f"Status changed from {old_status} to {new_status} by {user or 'System'}: {notes}"
        else:
            audit_note = f"Status changed from {old_status} to {new_status} by {user or 'System'}"

        if self.admin_notes:
            self.admin_notes += f"\n\n{audit_note}"
        else:
            self.admin_notes = audit_note

        self.save()

        # Send notification email
        self.send_status_notification(old_status, new_status)

        return True

    def send_status_notification(self, old_status, new_status):
        """Send email notification for status change"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.conf import settings
        from django.utils import timezone

        # Email templates for different status changes
        email_templates = {
            'confirmed': {
                'subject': f'Booking Confirmed - {self.booking_id.hex[:8].upper()}',
                'template': 'emails/booking_confirmed.html'
            },
            'in_progress': {
                'subject': f'Service Started - {self.booking_id.hex[:8].upper()}',
                'template': 'emails/booking_in_progress.html'
            },
            'completed': {
                'subject': f'Service Completed - {self.booking_id.hex[:8].upper()}',
                'template': 'emails/booking_completed.html'
            },
            'cancelled': {
                'subject': f'Booking Cancelled - {self.booking_id.hex[:8].upper()}',
                'template': 'emails/booking_cancelled.html'
            },
            'rescheduled': {
                'subject': f'Booking Rescheduled - {self.booking_id.hex[:8].upper()}',
                'template': 'emails/booking_rescheduled.html'
            }
        }

        if new_status in email_templates:
            template_info = email_templates[new_status]

            try:
                # Render HTML email if template exists
                html_content = None
                try:
                    html_content = render_to_string(template_info['template'], {
                        'booking': self,
                        'old_status': old_status,
                        'new_status': new_status,
                        'current_year': timezone.now().year,
                    })
                except:
                    # Template doesn't exist, use text only
                    pass

                # Plain text version
                text_content = f"""
Dear {self.contact_name},

Your booking status has been updated:

Booking ID: {self.booking_id.hex[:8].upper()}
Service: {self.service.name}
Status: {self.get_status_display()}
Date: {self.preferred_date}
Time: {self.get_preferred_time_slot_display()}

{self._get_status_message(new_status)}

If you have any questions, please contact us at:
Phone: +254 123 456 789
Email: info@globalcool-light.com

Best regards,
Global Cool-Light E.A LTD Team
                """

                # Create and send email
                if html_content:
                    email = EmailMultiAlternatives(
                        subject=template_info['subject'],
                        body=text_content,
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@globalcool-light.com'),
                        to=[self.contact_email],
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send(fail_silently=True)
                else:
                    # Fallback to simple text email
                    from django.core.mail import send_mail
                    send_mail(
                        subject=template_info['subject'],
                        message=text_content,
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@globalcool-light.com'),
                        recipient_list=[self.contact_email],
                        fail_silently=True,
                    )

            except Exception as e:
                # Log error but don't fail the status transition
                print(f"Failed to send status notification email: {e}")

    def _get_status_message(self, status):
        """Get appropriate message for status"""
        messages = {
            'confirmed': 'Your booking has been confirmed. Our team will contact you soon to finalize the details.',
            'in_progress': 'Our technician has started working on your service request.',
            'completed': 'Your service has been completed successfully. Thank you for choosing Global Cool-Light!',
            'cancelled': 'Your booking has been cancelled. If you have any questions, please contact us.',
            'rescheduled': 'Your booking has been rescheduled. We will contact you with the new date and time.',
        }
        return messages.get(status, 'Your booking status has been updated.')


class Inquiry(models.Model):
    """General inquiries and quote requests"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('quoted', 'Quoted'),
        ('converted', 'Converted to Booking'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Basic information
    inquiry_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='inquiries', null=True, blank=True)
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')

    # Contact details
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=17)

    # Inquiry details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget_range = models.CharField(max_length=100, blank=True, help_text="Client's budget range")
    timeline = models.CharField(max_length=100, blank=True, help_text="When they need the service")

    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')

    # Admin fields
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_inquiries')
    admin_notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry {self.inquiry_id.hex[:8]} - {self.contact_name} - {self.subject}"


class Quotation(models.Model):
    """Quotations for services"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('revised', 'Revised'),
    ]

    # Basic information
    quote_number = models.CharField(max_length=20, unique=True, blank=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='quotations', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='quotations')

    # Quote details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    items = models.JSONField(default=list, help_text="Quote items as JSON array")

    # Pricing
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=16.00, help_text="Tax percentage")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Terms and validity
    terms_and_conditions = models.TextField(blank=True)
    valid_until = models.DateField()
    payment_terms = models.CharField(max_length=200, default="50% deposit, 50% on completion")

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    sent_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    # Files
    pdf_file = models.FileField(upload_to='quotations/%Y/%m/', blank=True)

    # Admin fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_quotations')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Quote {self.quote_number} - {self.client.name} - KSh {self.total:,.2f}"

    def save(self, *args, **kwargs):
        if not self.quote_number:
            # Generate quote number: QT-YYYY-NNNN
            from datetime import datetime
            year = datetime.now().year
            last_quote = Quotation.objects.filter(
                quote_number__startswith=f'QT-{year}-'
            ).order_by('-quote_number').first()

            if last_quote:
                last_num = int(last_quote.quote_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.quote_number = f'QT-{year}-{new_num:04d}'

        # Calculate tax and total
        self.tax_amount = (self.subtotal * self.tax_rate) / 100
        self.total = self.subtotal + self.tax_amount - self.discount_amount

        super().save(*args, **kwargs)


class ChatSession(models.Model):
    """Model to track chat sessions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_chats', help_text="Admin user assigned to this chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat Session {self.session_id} - {self.name or 'Anonymous'}"

class ChatMessage(models.Model):
    """Model to store chat messages"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('agent', 'Agent'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."
