from django import forms
from django.forms import inlineformset_factory
from .models import Project, ProjectImage, Testimonial
from apps.services.models import Service


class ProjectForm(forms.ModelForm):
    """Form for creating and editing portfolio projects"""
    
    class Meta:
        model = Project
        fields = [
            'title', 'summary', 'description', 'client_name', 'location', 
            'project_type', 'services', 'start_date', 'end_date', 'duration_days',
            'status', 'completion_percentage', 'results_metrics', 'challenges_solved',
            'is_featured', 'is_published', 'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
                'required': True
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief project summary (max 500 characters)',
                'maxlength': 500
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Detailed project description'
            }),
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client or company name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project location (e.g., Nairobi, Kenya)'
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'services': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '5'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project duration in days',
                'min': '1'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'completion_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Completion percentage (0-100)',
                'min': '0',
                'max': '100'
            }),
            'results_metrics': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Project results and metrics (JSON format or text)'
            }),
            'challenges_solved': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Challenges solved during the project'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (max 60 characters)',
                'maxlength': 60
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (max 160 characters)',
                'maxlength': 160
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['services'].queryset = Service.objects.filter(is_active=True)
        self.fields['services'].help_text = "Hold Ctrl/Cmd to select multiple services"
        
        # Make certain fields optional for better UX
        self.fields['end_date'].required = False
        self.fields['duration_days'].required = False
        self.fields['results_metrics'].required = False
        self.fields['challenges_solved'].required = False
        self.fields['meta_title'].required = False
        self.fields['meta_description'].required = False


class ProjectImageForm(forms.ModelForm):
    """Form for individual project images"""
    
    class Meta:
        model = ProjectImage
        fields = ['image', 'title', 'description', 'image_type', 'is_featured', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image title (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Image description (optional)'
            }),
            'image_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order',
                'min': '0'
            }),
        }


# Create formset for handling multiple images
ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImage,
    form=ProjectImageForm,
    extra=3,  # Show 3 empty forms by default
    can_delete=True,
    fields=['image', 'title', 'description', 'image_type', 'is_featured', 'order']
)


class TestimonialForm(forms.ModelForm):
    """Form for creating and editing testimonials"""
    
    class Meta:
        model = Testimonial
        fields = [
            'author_name', 'author_title', 'author_company', 'author_image',
            'quote', 'rating', 'related_project', 'is_published', 'is_featured'
        ]
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author full name',
                'required': True
            }),
            'author_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title or position'
            }),
            'author_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company or organization'
            }),
            'author_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'quote': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Testimonial quote (max 1000 characters)',
                'maxlength': 1000,
                'required': True
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'related_project': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_project'].queryset = Project.objects.filter(is_published=True)
        self.fields['related_project'].empty_label = "Select a project (optional)"
        self.fields['related_project'].required = False


class PortfolioFilterForm(forms.Form):
    """Form for filtering portfolio projects on public pages"""
    
    PROJECT_TYPE_CHOICES = [
        ('', 'All Types'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('maintenance', 'Maintenance'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Status'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planning', 'Planning'),
    ]
    
    project_type = forms.ChoiceField(
        choices=PROJECT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    featured_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'this.form.submit()'
        })
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search projects...'
        })
    )
