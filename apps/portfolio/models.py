from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Project(models.Model):
    """Portfolio projects showcasing HVAC work"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = models.TextField(max_length=500, help_text="Brief project description")
    description = RichTextField(help_text="Detailed project description")

    # Project details
    client_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200)
    project_type = models.CharField(max_length=100, blank=True, help_text="e.g., Commercial, Residential")

    # Timeline
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)

    # Project status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    completion_percentage = models.PositiveIntegerField(default=100, help_text="0-100")

    # Services involved
    services = models.ManyToManyField('services.Service', blank=True, related_name='projects')

    # Results and metrics
    results_metrics = models.JSONField(default=dict, blank=True, help_text="Project outcomes as JSON")
    challenges_solved = models.TextField(blank=True)

    # Visibility
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Tracking
    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-is_featured', '-end_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})

    @property
    def duration_text(self):
        """Return human-readable duration"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            days = delta.days
            if days == 1:
                return "1 day"
            elif days < 30:
                return f"{days} days"
            elif days < 365:
                months = days // 30
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                years = days // 365
                return f"{years} year{'s' if years > 1 else ''}"
        elif self.duration_days:
            if self.duration_days == 1:
                return "1 day"
            elif self.duration_days < 30:
                return f"{self.duration_days} days"
            else:
                months = self.duration_days // 30
                return f"{months} month{'s' if months > 1 else ''}"
        return "Duration not specified"


class ProjectImage(models.Model):
    """Images for portfolio projects"""
    IMAGE_TYPES = [
        ('before', 'Before'),
        ('during', 'During Work'),
        ('after', 'After'),
        ('equipment', 'Equipment'),
        ('team', 'Team'),
        ('other', 'Other'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio/%Y/%m/')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='other')
    is_featured = models.BooleanField(default=False, help_text="Use as project thumbnail")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ['order', '-is_featured', 'created_at']

    def __str__(self):
        return f"{self.project.title} - {self.title or 'Image'}"


class Testimonial(models.Model):
    """Customer testimonials"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100, blank=True, help_text="Job title or company")
    author_company = models.CharField(max_length=100, blank=True)
    author_image = models.ImageField(upload_to='testimonials/', blank=True)

    quote = models.TextField(max_length=1000)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)

    # Optional project relation
    related_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')

    # Visibility
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.rating} stars"
