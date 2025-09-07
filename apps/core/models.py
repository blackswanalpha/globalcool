from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField


class SiteSettings(models.Model):
    """Global site settings and configuration"""

    # Company Information
    company_name = models.CharField(max_length=200, default="Global Cool-Light E.A LTD")
    tagline = models.CharField(max_length=200, default="Your Trusted HVAC Partner")
    description = RichTextField(
        default="Professional HVAC services in Kenya. We specialize in air conditioning installation, maintenance, and repair services."
    )

    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, default="+254 700 000 000")
    email = models.EmailField(default="info@globalcool-light.com")
    address = models.TextField(default="Nairobi, Kenya")

    # Business Hours
    working_hours = models.CharField(max_length=200, default="Mon-Fri: 8AM-6PM, Sat: 9AM-4PM")

    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    # SEO Settings
    meta_title = models.CharField(max_length=60, default="Global Cool-Light E.A LTD - Your Trusted HVAC Partner")
    meta_description = models.CharField(max_length=160, default="Professional HVAC services in Kenya. Installation, maintenance, and repair of air conditioning systems.")
    meta_keywords = models.CharField(max_length=200, default="HVAC, air conditioning, cooling, heating, Kenya, Nairobi")

    # Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True, null=True)
    google_maps_api_key = models.CharField(max_length=100, blank=True, null=True)

    # Maintenance Mode
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = RichTextField(
        default="We're currently performing scheduled maintenance. Please check back soon!",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.company_name} Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance is allowed")
        super().save(*args, **kwargs)


class FAQ(models.Model):
    """Frequently Asked Questions"""

    question = models.CharField(max_length=300)
    answer = RichTextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General'),
            ('services', 'Services'),
            ('pricing', 'Pricing'),
            ('maintenance', 'Maintenance'),
            ('installation', 'Installation'),
            ('repair', 'Repair'),
        ],
        default='general'
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    """Customer testimonials"""

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating} stars"


class ContactMessage(models.Model):
    """Contact form messages"""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    # Status tracking
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Admin notes
    admin_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class EmailTemplate(models.Model):
    """Email templates for various notifications"""

    TEMPLATE_TYPES = [
        ('booking_confirmation', 'Booking Confirmation'),
        ('booking_reminder', 'Booking Reminder'),
        ('quotation_sent', 'Quotation Sent'),
        ('quotation_accepted', 'Quotation Accepted'),
        ('quotation_rejected', 'Quotation Rejected'),
        ('service_completed', 'Service Completed'),
        ('payment_reminder', 'Payment Reminder'),
        ('welcome_email', 'Welcome Email'),
        ('password_reset', 'Password Reset'),
        ('general_notification', 'General Notification'),
    ]

    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=200)
    content = RichTextField(help_text="Use {{variable_name}} for dynamic content")

    # Available variables for each template type
    available_variables = models.TextField(
        blank=True,
        help_text="JSON list of available variables for this template"
    )

    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['template_type', 'name']
        unique_together = ['template_type', 'is_default']

    def __str__(self):
        return f"{self.get_template_type_display()} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one default template per type
        if self.is_default:
            EmailTemplate.objects.filter(
                template_type=self.template_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class SecuritySettings(models.Model):
    """Security configuration settings"""

    # Session settings
    session_timeout = models.PositiveIntegerField(
        default=3600,
        help_text="Session timeout in seconds (default: 3600 = 1 hour)"
    )
    remember_me_duration = models.PositiveIntegerField(
        default=1209600,
        help_text="Remember me duration in seconds (default: 1209600 = 2 weeks)"
    )

    # Login security
    max_login_attempts = models.PositiveIntegerField(
        default=5,
        help_text="Maximum failed login attempts before account lockout"
    )
    lockout_duration = models.PositiveIntegerField(
        default=900,
        help_text="Account lockout duration in seconds (default: 900 = 15 minutes)"
    )

    # Password policy
    password_min_length = models.PositiveIntegerField(default=8)
    password_require_uppercase = models.BooleanField(default=True)
    password_require_lowercase = models.BooleanField(default=True)
    password_require_numbers = models.BooleanField(default=True)
    password_require_symbols = models.BooleanField(default=False)
    password_expiry_days = models.PositiveIntegerField(
        default=0,
        help_text="Password expiry in days (0 = never expires)"
    )

    # Two-factor authentication
    enable_2fa = models.BooleanField(default=False)
    force_2fa_for_admins = models.BooleanField(default=False)

    # IP restrictions
    enable_ip_whitelist = models.BooleanField(default=False)
    allowed_ips = models.TextField(
        blank=True,
        help_text="Comma-separated list of allowed IP addresses"
    )

    # Audit logging
    log_login_attempts = models.BooleanField(default=True)
    log_admin_actions = models.BooleanField(default=True)
    log_retention_days = models.PositiveIntegerField(
        default=90,
        help_text="Number of days to retain security logs"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Security Settings"
        verbose_name_plural = "Security Settings"

    def __str__(self):
        return "Security Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SecuritySettings.objects.exists():
            raise ValueError("Only one SecuritySettings instance is allowed")
        super().save(*args, **kwargs)
