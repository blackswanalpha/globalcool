from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    # Booking URLs
    path('booking/', views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/<slug:service_slug>/', views.BookingCreateView.as_view(), name='booking_create_service'),
    path('booking/success/', views.BookingSuccessView.as_view(), name='booking_success'),

    # Inquiry URLs
    path('inquiry/', views.InquiryCreateView.as_view(), name='inquiry_create'),
    path('inquiry/success/', views.InquirySuccessView.as_view(), name='inquiry_success'),

    # Quote request URL
    path('quote/', views.QuoteRequestView.as_view(), name='quote'),

    # Chat URLs
    path('chat/message/', views.ChatMessageView.as_view(), name='chat_message'),
    path('chat/history/<str:session_id>/', views.ChatHistoryView.as_view(), name='chat_history'),
]
