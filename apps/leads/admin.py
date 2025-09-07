from django.contrib import admin
from .models import ChatSession, ChatMessage, Client, Booking, Inquiry, Quotation

# Register your models here.

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('message_type', 'content', 'timestamp', 'is_read')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'name', 'email', 'phone', 'is_active', 'created_at', 'message_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('session_id', 'name', 'email', 'phone')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    inlines = [ChatMessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_type', 'content_preview', 'timestamp', 'is_read')
    list_filter = ('message_type', 'timestamp', 'is_read')
    search_fields = ('content', 'session__session_id', 'session__name')
    readonly_fields = ('timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'client_type', 'total_bookings', 'total_spent', 'created_at']
    list_filter = ['client_type', 'preferred_contact_method', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company_name']
    readonly_fields = ['total_bookings', 'total_spent', 'created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'contact_name', 'service', 'preferred_date', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'source', 'preferred_date', 'created_at']
    search_fields = ['contact_name', 'contact_email', 'contact_phone']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    date_hierarchy = 'preferred_date'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['inquiry_id', 'contact_name', 'subject', 'service', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['contact_name', 'contact_email', 'subject']
    readonly_fields = ['inquiry_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quote_number', 'client', 'title', 'total', 'status', 'valid_until', 'created_at']
    list_filter = ['status', 'created_at', 'valid_until']
    search_fields = ['quote_number', 'title', 'client__name']
    readonly_fields = ['quote_number', 'tax_amount', 'total', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
