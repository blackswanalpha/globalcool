"""
URL configuration for Global Cool-Light E.A LTD project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Core app (main pages)
    path('', include('apps.core.urls')),

    # Other apps
    path('services/', include('apps.services.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('blog/', include('apps.blog.urls')),
    path('leads/', include('apps.leads.urls')),
    path('users/', include('apps.users.urls')),

    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Direct booking access for better UX
    path('booking/', RedirectView.as_view(url='/leads/booking/', permanent=True)),
    path('quote/', RedirectView.as_view(url='/leads/inquiry/', permanent=True)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
