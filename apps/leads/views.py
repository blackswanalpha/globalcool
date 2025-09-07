from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
import json
import uuid
from .models import ChatSession, ChatMessage, Booking, Inquiry, Client
from .forms import BookingForm, InquiryForm, QuickBookingForm
from apps.services.models import Service


class QuoteRequestView(CreateView):
    """Handle quote requests by creating inquiries"""
    model = Inquiry
    form_class = InquiryForm
    template_name = 'leads/quote.html'
    success_url = reverse_lazy('leads:inquiry_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        inquiry.status = 'new'
        if not inquiry.subject:
            inquiry.subject = f"Quote Request - {inquiry.service.name if inquiry.service else 'General'}"
        inquiry.save()

        # Send confirmation email
        self.send_inquiry_confirmation(inquiry)

        # Store inquiry ID in session
        self.request.session['inquiry_id'] = str(inquiry.inquiry_id)

        messages.success(
            self.request,
            f'Your quote request has been submitted successfully! '
            f'Reference ID: {inquiry.inquiry_id.hex[:8].upper()}. '
            f'We will prepare your quotation within 24 hours.'
        )

        return super().form_valid(form)

    def send_inquiry_confirmation(self, inquiry):
        """Send confirmation email to customer"""
        try:
            subject = f'Quote Request Received - {inquiry.inquiry_id.hex[:8].upper()}'
            message = f"""
Dear {inquiry.contact_name},

Thank you for your quote request. We have received your inquiry and will prepare a detailed quotation for you.

Reference ID: {inquiry.inquiry_id.hex[:8].upper()}
Service: {inquiry.service.name if inquiry.service else 'General'}
Submitted: {inquiry.created_at.strftime('%B %d, %Y at %I:%M %p')}

Our team will review your requirements and send you a comprehensive quotation within 24 hours.

Best regards,
Global Cool-Light E.A LTD Team
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [inquiry.contact_email],
                fail_silently=True,
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send confirmation email: {e}")


class BookingCreateView(CreateView):
    """Create a new service booking"""
    model = Booking
    form_class = BookingForm
    template_name = 'leads/booking_form.html'
    success_url = reverse_lazy('leads:booking_success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass service slug if provided in URL
        kwargs['service_slug'] = self.kwargs.get('service_slug')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add service information if service_slug is provided
        service_slug = self.kwargs.get('service_slug')
        if service_slug:
            try:
                service = Service.objects.get(slug=service_slug, is_active=True)
                context['selected_service'] = service
            except Service.DoesNotExist:
                pass

        # Add all active services for the dropdown
        context['services'] = Service.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        # Set default values
        booking = form.save(commit=False)
        booking.source = 'website'
        booking.status = 'new'
        booking.save()

        # Send confirmation email
        self.send_booking_confirmation(booking)

        # Store booking ID in session for success page
        self.request.session['booking_id'] = str(booking.booking_id)

        messages.success(
            self.request,
            f'Your booking request has been submitted successfully! '
            f'Booking ID: {booking.booking_id.hex[:8].upper()}. '
            f'We will contact you shortly to confirm the details.'
        )

        return super().form_valid(form)

    def send_booking_confirmation(self, booking):
        """Send booking confirmation email to customer"""
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import render_to_string

            subject = f'Booking Confirmation - {booking.booking_id.hex[:8].upper()}'

            # Render HTML email
            html_content = render_to_string('emails/booking_confirmation.html', {
                'booking': booking,
                'current_year': timezone.now().year,
            })

            # Plain text fallback
            text_content = f"""
Dear {booking.contact_name},

Thank you for booking with Global Cool-Light E.A LTD!

Booking Details:
- Booking ID: {booking.booking_id.hex[:8].upper()}
- Service: {booking.service.name}
- Preferred Date: {booking.preferred_date.strftime('%B %d, %Y')}
- Preferred Time: {booking.get_preferred_time_slot_display()}
- Location: {booking.location_address}

Our team will contact you within 24 hours to confirm the booking details and schedule.

For any questions, please contact us:
- Phone: +254 123 456 789
- Email: info@globalcool-light.com

Best regards,
Global Cool-Light E.A LTD Team
            """

            # Create email with both HTML and text versions
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[booking.contact_email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)

        except Exception as e:
            # Log error but don't fail the booking
            print(f"Failed to send booking confirmation email: {e}")


class BookingSuccessView(TemplateView):
    """Booking success confirmation page"""
    template_name = 'leads/booking_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get booking from session
        booking_id = self.request.session.get('booking_id')
        if booking_id:
            try:
                booking = Booking.objects.get(booking_id=booking_id)
                context['booking'] = booking
                # Clear booking ID from session
                del self.request.session['booking_id']
            except Booking.DoesNotExist:
                pass

        return context


class InquiryCreateView(CreateView):
    """Create a new inquiry/quote request"""
    model = Inquiry
    form_class = InquiryForm
    template_name = 'leads/inquiry_form.html'
    success_url = reverse_lazy('leads:inquiry_success')

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        inquiry.source = 'website'
        inquiry.status = 'new'
        inquiry.save()

        # Send confirmation email
        self.send_inquiry_confirmation(inquiry)

        # Store inquiry ID in session
        self.request.session['inquiry_id'] = str(inquiry.inquiry_id)

        messages.success(
            self.request,
            f'Your inquiry has been submitted successfully! '
            f'Reference ID: {inquiry.inquiry_id.hex[:8].upper()}. '
            f'We will respond within 24 hours.'
        )

        return super().form_valid(form)

    def send_inquiry_confirmation(self, inquiry):
        """Send inquiry confirmation email"""
        try:
            subject = f'Inquiry Received - {inquiry.subject}'
            message = f"""
Dear {inquiry.contact_name},

Thank you for your inquiry with Global Cool-Light E.A LTD!

Inquiry Details:
- Reference ID: {inquiry.inquiry_id.hex[:8].upper()}
- Subject: {inquiry.subject}
- Service: {inquiry.service.name if inquiry.service else 'General Inquiry'}
- Priority: {inquiry.get_priority_display()}

Your Message:
{inquiry.message}

Our team will review your inquiry and respond within 24 hours.

Best regards,
Global Cool-Light E.A LTD Team
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [inquiry.contact_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send inquiry confirmation email: {e}")


class InquirySuccessView(TemplateView):
    """Inquiry success confirmation page"""
    template_name = 'leads/inquiry_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get inquiry from session
        inquiry_id = self.request.session.get('inquiry_id')
        if inquiry_id:
            try:
                inquiry = Inquiry.objects.get(inquiry_id=inquiry_id)
                context['inquiry'] = inquiry
                # Clear inquiry ID from session
                del self.request.session['inquiry_id']
            except Inquiry.DoesNotExist:
                pass

        return context


@method_decorator(csrf_exempt, name='dispatch')
class ChatMessageView(View):
    """Handle chat messages via HTMX/AJAX"""

    def post(self, request):
        try:
            data = json.loads(request.body)
            message_content = data.get('message', '').strip()
            session_id = data.get('session_id')
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()

            if not message_content:
                return JsonResponse({'error': 'Message content is required'}, status=400)

            # Validate contact information for new sessions
            if not session_id:
                if not name or not email:
                    return JsonResponse({'error': 'Name and email are required to start a chat'}, status=400)
                session_id = str(uuid.uuid4())

            # Get or create chat session
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'is_active': True,
                    'name': name,
                    'email': email,
                    'phone': phone
                }
            )

            # Update contact information if session exists but doesn't have it
            if not created and not session.name and name:
                session.name = name
                session.email = email
                session.phone = phone
                session.save()

            # Save user message
            user_message = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=message_content
            )

            # Generate bot response
            bot_response = self.generate_bot_response(message_content)

            # Save bot message
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=bot_response
            )

            return JsonResponse({
                'success': True,
                'session_id': session_id,
                'user_message': {
                    'id': user_message.id,
                    'content': user_message.content,
                    'timestamp': user_message.timestamp.isoformat()
                },
                'bot_message': {
                    'id': bot_message.id,
                    'content': bot_message.content,
                    'timestamp': bot_message.timestamp.isoformat()
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def generate_bot_response(self, user_message):
        """Generate automated bot responses based on keywords"""
        message_lower = user_message.lower()

        # Keyword-based responses
        if any(word in message_lower for word in ['price', 'cost', 'quote', 'estimate']):
            return "I'd be happy to help you with pricing! For an accurate quote, please provide details about your HVAC needs, property size, and preferred service type. Our team will prepare a custom estimate for you."

        elif any(word in message_lower for word in ['service', 'repair', 'maintenance', 'installation']):
            return "We offer comprehensive HVAC services including installation, repair, maintenance, and emergency services. What specific service are you looking for? Our certified technicians are ready to help!"

        elif any(word in message_lower for word in ['emergency', 'urgent', 'broken', 'not working']):
            return "For emergency HVAC services, please call us directly at +254 700 000 000. We provide 24/7 emergency support and can dispatch a technician to your location quickly."

        elif any(word in message_lower for word in ['hours', 'time', 'schedule', 'appointment']):
            return "We're open Monday to Friday 8:00 AM - 6:00 PM, and Saturday 9:00 AM - 4:00 PM. For emergency services, we're available 24/7. Would you like to schedule an appointment?"

        elif any(word in message_lower for word in ['location', 'area', 'service area', 'where']):
            return "We serve the greater Nairobi area and surrounding regions. Our service areas include Nairobi, Kiambu, Machakos, and Kajiado counties. Please let us know your location to confirm service availability."

        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! Welcome to Global Cool-Light E.A LTD. We're your trusted HVAC specialists. How can we help you today? Whether you need installation, repair, or maintenance services, we're here to assist!"

        else:
            return "Thank you for your message! Our team will review your inquiry and get back to you shortly. For immediate assistance, please call us at +254 700 000 000 or use our WhatsApp chat."


class ChatHistoryView(View):
    """Get chat history for a session"""

    def get(self, request, session_id):
        try:
            session = get_object_or_404(ChatSession, session_id=session_id)
            messages = session.messages.all()

            message_data = []
            for message in messages:
                message_data.append({
                    'id': message.id,
                    'type': message.message_type,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat()
                })

            return JsonResponse({
                'success': True,
                'session_id': session_id,
                'messages': message_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
