from django.urls import path
from . import views
from apps.portfolio import views as portfolio_views

app_name = 'users'

urlpatterns = [
    # Admin splashscreen and authentication
    path('admin/', views.admin_splashscreen, name='admin_splashscreen'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/signup/', views.admin_signup, name='admin_signup'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/forgot-password/', views.forgot_password, name='forgot_password'),

    # Admin dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admin booking management
    path('admin/bookings/', views.admin_bookings_list, name='admin_bookings_list'),
    path('admin/bookings/<uuid:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),

    # Admin quotation management
    path('admin/quotations/', views.admin_quotations_list, name='admin_quotations_list'),
    path('admin/quotations/create/', views.admin_quotation_create, name='admin_quotation_create'),
    path('admin/quotations/<int:quotation_id>/', views.admin_quotation_detail, name='admin_quotation_detail'),
    path('admin/quotations/<int:quotation_id>/edit/', views.admin_quotation_edit, name='admin_quotation_edit'),
    path('admin/quotations/<int:quotation_id>/delete/', views.admin_quotation_delete, name='admin_quotation_delete'),
    path('admin/quotations/<int:quotation_id>/send-email/', views.admin_quotation_send_email, name='admin_quotation_send_email'),
    path('admin/quotations/<int:quotation_id>/update-status/', views.admin_quotation_status_update, name='admin_quotation_status_update'),

    # Inquiry to quotation conversion
    path('admin/inquiries/<uuid:inquiry_id>/convert-to-quotation/', views.admin_inquiry_to_quotation, name='admin_inquiry_to_quotation'),

    # Admin services & products management
    path('admin/services-products/', views.admin_services_products, name='admin_services_products'),

    # Service CRUD
    path('admin/services/add/', views.admin_service_add, name='admin_service_add'),
    path('admin/services/<int:service_id>/', views.admin_service_view, name='admin_service_view'),
    path('admin/services/<int:service_id>/edit/', views.admin_service_edit, name='admin_service_edit'),
    path('admin/services/<int:service_id>/delete/', views.admin_service_delete, name='admin_service_delete'),

    # Product CRUD
    path('admin/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin/products/<int:product_id>/', views.admin_product_view, name='admin_product_view'),
    path('admin/products/<int:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin/products/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),

    # Admin portfolio management
    path('admin/portfolio/', portfolio_views.admin_portfolio_list, name='admin_portfolio_list'),
    path('admin/portfolio/add/', portfolio_views.admin_portfolio_add, name='admin_portfolio_add'),
    path('admin/portfolio/<int:project_id>/', portfolio_views.admin_portfolio_detail, name='admin_portfolio_detail'),
    path('admin/portfolio/<int:project_id>/edit/', portfolio_views.admin_portfolio_edit, name='admin_portfolio_edit'),
    path('admin/portfolio/<int:project_id>/delete/', portfolio_views.admin_portfolio_delete, name='admin_portfolio_delete'),

    # Portfolio AJAX actions
    path('admin/portfolio/<int:project_id>/toggle-featured/', portfolio_views.admin_portfolio_toggle_featured, name='admin_portfolio_toggle_featured'),
    path('admin/portfolio/<int:project_id>/toggle-published/', portfolio_views.admin_portfolio_toggle_published, name='admin_portfolio_toggle_published'),

    # Customer CRUD
    path('admin/customers/', views.admin_customers_list, name='admin_customers_list'),
    path('admin/customers/add/', views.admin_customer_add, name='admin_customer_add'),
    path('admin/customers/<int:customer_id>/', views.admin_customer_view, name='admin_customer_view'),
    path('admin/customers/<int:customer_id>/edit/', views.admin_customer_edit, name='admin_customer_edit'),
    path('admin/customers/<int:customer_id>/delete/', views.admin_customer_delete, name='admin_customer_delete'),

    # Testimonial management
    path('admin/testimonials/add/', portfolio_views.admin_testimonial_add, name='admin_testimonial_add'),

    # Settings management
    path('admin/settings/', views.admin_settings_general, name='admin_settings_general'),
    path('admin/settings/general/', views.admin_settings_general, name='admin_settings_general'),
    path('admin/settings/account/', views.admin_account_settings, name='admin_account_settings'),
    path('admin/settings/preferences/', views.admin_preferences, name='admin_preferences'),
    path('admin/settings/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/settings/users/add/', views.admin_user_add, name='admin_user_add'),
    path('admin/settings/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/settings/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/settings/email-templates/', views.admin_email_templates, name='admin_email_templates'),
    path('admin/settings/security/', views.admin_security_settings, name='admin_security_settings'),

    # Leads management
    path('admin/leads/', views.admin_leads_list, name='admin_leads_list'),
    path('admin/leads/respond/', views.admin_lead_respond, name='admin_lead_respond'),
    path('admin/leads/status-update/', views.admin_lead_status_update, name='admin_lead_status_update'),
    path('admin/leads/<str:session_id>/', views.admin_lead_detail, name='admin_lead_detail'),

    # Profile management (referenced in sidebar)
    path('admin/profile/', views.admin_profile, name='admin_profile'),
]
