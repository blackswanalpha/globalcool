from django import forms
from .models import ContactMessage, SiteSettings, EmailTemplate, SecuritySettings


class ContactForm(forms.ModelForm):
    """Contact form for the website"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+254 700 000 000',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What can we help you with?',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell us more about your HVAC needs...',
                'rows': 5,
                'required': True,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add labels
        self.fields['name'].label = 'Full Name'
        self.fields['email'].label = 'Email Address'
        self.fields['phone'].label = 'Phone Number (Optional)'
        self.fields['subject'].label = 'Subject'
        self.fields['message'].label = 'Message'
        
        # Add help text
        self.fields['phone'].help_text = 'We may call you to discuss your requirements'
        self.fields['message'].help_text = 'Please provide as much detail as possible about your HVAC needs'
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message


class SiteSettingsForm(forms.ModelForm):
    """Form for site settings configuration"""

    class Meta:
        model = SiteSettings
        fields = [
            'company_name', 'tagline', 'description', 'phone', 'email', 'address',
            'working_hours', 'facebook_url', 'twitter_url', 'linkedin_url',
            'instagram_url', 'youtube_url', 'meta_title', 'meta_description',
            'meta_keywords', 'google_analytics_id', 'google_maps_api_key',
            'maintenance_mode', 'maintenance_message'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Tagline'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 700 000 000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'info@company.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Company Address'
            }),
            'working_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mon-Fri: 8AM-6PM, Sat: 9AM-4PM'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/yourpage'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/yourhandle'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/company/yourcompany'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/yourhandle'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/yourchannel'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO Title (max 60 characters)',
                'maxlength': 60
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'SEO Description (max 160 characters)',
                'maxlength': 160
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'keyword1, keyword2, keyword3'
            }),
            'google_analytics_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GA-XXXXXXXXX-X'
            }),
            'google_maps_api_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Google Maps API Key'
            }),
            'maintenance_mode': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class EmailTemplateForm(forms.ModelForm):
    """Form for email template management"""

    class Meta:
        model = EmailTemplate
        fields = ['name', 'template_type', 'subject', 'content', 'is_active', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Template Name'
            }),
            'template_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Subject'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class SecuritySettingsForm(forms.ModelForm):
    """Form for security settings configuration"""

    class Meta:
        model = SecuritySettings
        fields = [
            'session_timeout', 'remember_me_duration', 'max_login_attempts',
            'lockout_duration', 'password_min_length', 'password_require_uppercase',
            'password_require_lowercase', 'password_require_numbers',
            'password_require_symbols', 'password_expiry_days', 'enable_2fa',
            'force_2fa_for_admins', 'enable_ip_whitelist', 'allowed_ips',
            'log_login_attempts', 'log_admin_actions', 'log_retention_days'
        ]
        widgets = {
            'session_timeout': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 300,  # 5 minutes minimum
                'max': 86400,  # 24 hours maximum
            }),
            'remember_me_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 86400,  # 1 day minimum
                'max': 2592000,  # 30 days maximum
            }),
            'max_login_attempts': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 3,
                'max': 10,
            }),
            'lockout_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 300,  # 5 minutes minimum
                'max': 3600,  # 1 hour maximum
            }),
            'password_min_length': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 6,
                'max': 20,
            }),
            'password_require_uppercase': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'password_require_lowercase': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'password_require_numbers': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'password_require_symbols': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'password_expiry_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 365,
            }),
            'enable_2fa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'force_2fa_for_admins': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'enable_ip_whitelist': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'allowed_ips': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '192.168.1.1, 10.0.0.1, 203.0.113.1'
            }),
            'log_login_attempts': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'log_admin_actions': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'log_retention_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 30,
                'max': 365,
            }),
        }

    def clean_allowed_ips(self):
        allowed_ips = self.cleaned_data.get('allowed_ips', '')
        if self.cleaned_data.get('enable_ip_whitelist') and not allowed_ips.strip():
            raise forms.ValidationError('IP addresses are required when IP whitelist is enabled.')
        return allowed_ips
