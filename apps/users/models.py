from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile for staff members"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('sales', 'Sales Representative'),
        ('support', 'Customer Support'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='support')

    # Contact information
    phone = models.CharField(max_length=17, blank=True)
    address = models.TextField(blank=True)

    # Professional details
    employee_id = models.CharField(max_length=20, blank=True, unique=True)
    department = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)

    # Profile image
    avatar = models.ImageField(upload_to='profiles/', blank=True)

    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    # Bio and skills
    bio = models.TextField(blank=True, max_length=500)
    skills = models.TextField(blank=True, help_text="Skills and certifications, one per line")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"

    @property
    def skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [s.strip() for s in self.skills.split('\n') if s.strip()]
        return []


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
