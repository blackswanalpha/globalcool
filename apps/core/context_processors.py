from django.conf import settings
from .models import SiteSettings
import datetime


def site_settings(request):
    """
    Context processor to make site settings available in all templates
    """
    try:
        site_settings_obj = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings_obj = None
    
    return {
        'site_settings': site_settings_obj,
        'current_year': datetime.datetime.now().year,
        'brand_colors': getattr(settings, 'BRAND_COLORS', {}),
        'company_info': getattr(settings, 'COMPANY_INFO', {}),
    }
