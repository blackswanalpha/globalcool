from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Legal pages
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),
    
    # Test page
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),

    # AJAX endpoints
    path('ajax/contact/', views.ajax_contact_form, name='ajax_contact'),
]
