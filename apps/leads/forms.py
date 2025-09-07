from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from .models import ChatSession, ChatMessage, Booking, Inquiry, Client, Quotation
from apps.services.models import Service
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    """Form for creating service bookings from public pages"""
    
    class Meta:
        model = Booking
        fields = [
            'service', 'contact_name', 'contact_email', 'contact_phone',
            'preferred_date', 'preferred_time_slot', 'location_address',
            'message', 'priority'
        ]
        widgets = {
            'contact_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'required': True
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+254 700 000 000',
                'required': True
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'required': True,
                'min': date.today().isoformat()
            }),
            'preferred_time_slot': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'location_address': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Please provide your complete address including landmarks',
                'rows': 3,
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Please describe your HVAC needs, any specific requirements, or additional information',
                'rows': 4
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'service': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        labels = {
            'contact_name': 'Full Name',
            'contact_email': 'Email Address',
            'contact_phone': 'Phone Number',
            'preferred_date': 'Preferred Date',
            'preferred_time_slot': 'Preferred Time',
            'location_address': 'Service Location',
            'message': 'Additional Information',
            'priority': 'Priority Level',
            'service': 'Service Required'
        }
        help_texts = {
            'contact_phone': 'We will call you to confirm the booking',
            'preferred_date': 'Select your preferred service date',
            'location_address': 'Complete address where service is needed',
            'message': 'Any specific requirements or additional details',
            'priority': 'How urgent is this service request?'
        }

    def __init__(self, *args, **kwargs):
        service_slug = kwargs.pop('service_slug', None)
        super().__init__(*args, **kwargs)
        
        # Filter active services only
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        
        # Pre-select service if provided
        if service_slug:
            try:
                service = Service.objects.get(slug=service_slug, is_active=True)
                self.fields['service'].initial = service
            except Service.DoesNotExist:
                pass

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date:
            if preferred_date < date.today():
                raise ValidationError("Booking date cannot be in the past.")
            
            # Don't allow bookings more than 3 months in advance
            max_date = date.today() + timedelta(days=90)
            if preferred_date > max_date:
                raise ValidationError("Bookings can only be made up to 3 months in advance.")
        
        return preferred_date

    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        if phone:
            # Basic phone validation - remove spaces and check format
            phone = phone.replace(' ', '').replace('-', '')
            if not phone.startswith('+'):
                if phone.startswith('0'):
                    phone = '+254' + phone[1:]
                elif phone.startswith('7') or phone.startswith('1'):
                    phone = '+254' + phone
            
            # Validate Kenyan phone number format
            if not (phone.startswith('+254') and len(phone) == 13):
                raise ValidationError("Please enter a valid Kenyan phone number (e.g., +254 700 000 000)")
        
        return phone

    def clean_contact_name(self):
        name = self.cleaned_data.get('contact_name')
        if name:
            name = name.strip()
            if len(name.split()) < 2:
                raise ValidationError("Please enter your full name (first and last name).")
        return name


class InquiryForm(forms.ModelForm):
    """Form for general inquiries and quote requests"""
    
    class Meta:
        model = Inquiry
        fields = [
            'contact_name', 'contact_email', 'contact_phone',
            'subject', 'service', 'message', 'priority'
        ]
        widgets = {
            'contact_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'required': True
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+254 700 000 000'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Brief subject of your inquiry',
                'required': True
            }),
            'service': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Please provide detailed information about your HVAC needs, property details, and any specific requirements',
                'rows': 6,
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'contact_name': 'Full Name',
            'contact_email': 'Email Address',
            'contact_phone': 'Phone Number (Optional)',
            'subject': 'Subject',
            'service': 'Related Service (Optional)',
            'message': 'Your Inquiry',
            'priority': 'Priority Level'
        }
        help_texts = {
            'contact_phone': 'We may call you to discuss your requirements',
            'service': 'Select if your inquiry is about a specific service',
            'message': 'Please provide as much detail as possible',
            'priority': 'How urgent is this inquiry?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add empty option for service field
        service_choices = [('', 'Select a service (optional)')] + list(
            Service.objects.filter(is_active=True).values_list('id', 'name')
        )
        self.fields['service'].choices = service_choices
        self.fields['service'].required = False

    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        if phone:
            # Same phone validation as BookingForm
            phone = phone.replace(' ', '').replace('-', '')
            if not phone.startswith('+'):
                if phone.startswith('0'):
                    phone = '+254' + phone[1:]
                elif phone.startswith('7') or phone.startswith('1'):
                    phone = '+254' + phone
            
            if not (phone.startswith('+254') and len(phone) == 13):
                raise ValidationError("Please enter a valid Kenyan phone number (e.g., +254 700 000 000)")
        
        return phone


class QuickBookingForm(forms.Form):
    """Simplified booking form for quick bookings"""
    
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your full name',
            'required': True
        }),
        label='Full Name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your.email@example.com',
            'required': True
        }),
        label='Email Address'
    )
    
    phone = forms.CharField(
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+254 700 000 000',
            'required': True
        }),
        label='Phone Number'
    )
    
    service_type = forms.ChoiceField(
        choices=[
            ('installation', 'AC Installation'),
            ('repair', 'AC Repair'),
            ('maintenance', 'AC Maintenance'),
            ('consultation', 'Consultation'),
            ('other', 'Other Service')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        }),
        label='Service Type'
    )
    
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
            'required': True,
            'min': date.today().isoformat()
        }),
        label='Preferred Date'
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Brief description of your needs',
            'rows': 3
        }),
        label='Message',
        required=False
    )

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < date.today():
            raise ValidationError("Booking date cannot be in the past.")
        return preferred_date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = phone.replace(' ', '').replace('-', '')
            if not phone.startswith('+'):
                if phone.startswith('0'):
                    phone = '+254' + phone[1:]
                elif phone.startswith('7') or phone.startswith('1'):
                    phone = '+254' + phone
            
            if not (phone.startswith('+254') and len(phone) == 13):
                raise ValidationError("Please enter a valid Kenyan phone number")
        
        return phone


class QuotationForm(forms.ModelForm):
    """Form for creating and editing quotations in admin portal"""

    class Meta:
        model = Quotation
        fields = [
            'client', 'inquiry', 'title', 'description', 'items',
            'subtotal', 'tax_rate', 'discount_amount', 'valid_until',
            'terms_and_conditions', 'notes'
        ]
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'inquiry': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quotation title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the quotation',
                'rows': 3
            }),
            'items': forms.HiddenInput(),  # Will be handled by JavaScript
            'subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'readonly': True
            }),
            'tax_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'value': '16.00'
            }),
            'discount_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '0.00'
            }),
            'valid_until': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Terms and conditions for this quotation',
                'rows': 4
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Internal notes (not visible to client)',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default valid_until to 30 days from now
        if not self.instance.pk:
            self.fields['valid_until'].initial = (timezone.now().date() + timedelta(days=30))

        # Order clients by name
        self.fields['client'].queryset = Client.objects.all().order_by('name')

        # Filter inquiries to only unprocessed ones
        self.fields['inquiry'].queryset = Inquiry.objects.filter(
            status__in=['new', 'in_review']
        ).order_by('-created_at')
        self.fields['inquiry'].empty_label = "Select an inquiry (optional)"

        # Add help text
        self.fields['items'].help_text = "Line items will be managed through the interface below"
        self.fields['tax_rate'].help_text = "Tax percentage (default: 16% VAT)"
        self.fields['discount_amount'].help_text = "Fixed discount amount in KSh"

    def clean_valid_until(self):
        valid_until = self.cleaned_data.get('valid_until')
        if valid_until and valid_until <= timezone.now().date():
            raise ValidationError("Valid until date must be in the future.")
        return valid_until

    def clean_tax_rate(self):
        tax_rate = self.cleaned_data.get('tax_rate')
        if tax_rate is not None and (tax_rate < 0 or tax_rate > 100):
            raise ValidationError("Tax rate must be between 0 and 100 percent.")
        return tax_rate

    def clean_discount_amount(self):
        discount_amount = self.cleaned_data.get('discount_amount')
        if discount_amount is not None and discount_amount < 0:
            raise ValidationError("Discount amount cannot be negative.")
        return discount_amount

    def clean(self):
        cleaned_data = super().clean()
        subtotal = cleaned_data.get('subtotal', 0)
        discount_amount = cleaned_data.get('discount_amount', 0)

        if discount_amount and subtotal and discount_amount > subtotal:
            raise ValidationError("Discount amount cannot be greater than subtotal.")

        return cleaned_data


class ClientForm(forms.ModelForm):
    """Form for creating and editing clients in admin portal"""

    class Meta:
        model = Client
        fields = [
            'name', 'client_type', 'email', 'phone', 'company_name',
            'address', 'preferred_contact_method', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name or company name',
                'required': True
            }),
            'client_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'client@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 700 000 000',
                'required': True
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name (if applicable)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Complete address including city and postal code',
                'rows': 3
            }),
            'preferred_contact_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Internal notes about this client',
                'rows': 4
            })
        }
        labels = {
            'name': 'Full Name / Company Name',
            'client_type': 'Client Type',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'company_name': 'Company Name',
            'address': 'Address',
            'preferred_contact_method': 'Preferred Contact Method',
            'notes': 'Internal Notes'
        }
        help_texts = {
            'name': 'Full name for individuals or company name for businesses',
            'client_type': 'Select the type of client',
            'email': 'Primary email address for communication',
            'phone': 'Primary phone number',
            'company_name': 'Leave blank for individual clients',
            'address': 'Complete physical address',
            'preferred_contact_method': 'How the client prefers to be contacted',
            'notes': 'Internal notes visible only to staff'
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Same phone validation as other forms
            phone = phone.replace(' ', '').replace('-', '')
            if not phone.startswith('+'):
                if phone.startswith('0'):
                    phone = '+254' + phone[1:]
                elif phone.startswith('7') or phone.startswith('1'):
                    phone = '+254' + phone

            if not (phone.startswith('+254') and len(phone) == 13):
                raise ValidationError("Please enter a valid Kenyan phone number (e.g., +254 700 000 000)")

        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (excluding current instance)
            existing_client = Client.objects.filter(email=email)
            if self.instance.pk:
                existing_client = existing_client.exclude(pk=self.instance.pk)

            if existing_client.exists():
                raise ValidationError("A client with this email address already exists.")

        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise ValidationError("Name must be at least 2 characters long.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        client_type = cleaned_data.get('client_type')
        company_name = cleaned_data.get('company_name')

        # If client type is business, company name should be provided
        if client_type in ['business', 'government', 'ngo'] and not company_name:
            raise ValidationError({
                'company_name': 'Company name is required for business, government, and NGO clients.'
            })

        return cleaned_data
