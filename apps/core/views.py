from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import FAQ, Testimonial, ContactMessage
from .forms import ContactForm


class HomeView(TemplateView):
    """Home page view"""
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_testimonials': Testimonial.objects.filter(
                is_active=True, is_featured=True
            )[:3],
            'faqs': FAQ.objects.filter(is_active=True)[:6],
        })
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        })
        return context


class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact_message = form.save()

            # Send email notification (optional)
            try:
                send_mail(
                    subject=f"New Contact Form Submission: {contact_message.subject}",
                    message=f"""
                    New contact form submission from {contact_message.name}

                    Email: {contact_message.email}
                    Phone: {contact_message.phone}
                    Subject: {contact_message.subject}

                    Message:
                    {contact_message.message}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Log error in production

            messages.success(
                request,
                "Thank you for your message! We'll get back to you soon."
            )
            return redirect('core:contact')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class PrivacyView(TemplateView):
    """Privacy policy page"""
    template_name = 'pages/privacy.html'


class TermsView(TemplateView):
    """Terms of service page"""
    template_name = 'pages/terms.html'


class SitemapView(TemplateView):
    """Sitemap page"""
    template_name = 'pages/sitemap.html'


def ajax_contact_form(request):
    """HTMX contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send email notification
            try:
                send_mail(
                    subject=f"New Contact Form Submission: {contact_message.subject}",
                    message=f"""
                    New contact form submission from {contact_message.name}

                    Email: {contact_message.email}
                    Phone: {contact_message.phone}
                    Subject: {contact_message.subject}

                    Message:
                    {contact_message.message}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            return JsonResponse({
                'success': True,
                'message': "Thank you for your message! We'll get back to you soon."
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
