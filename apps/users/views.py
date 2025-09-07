from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from django.http import JsonResponse
import json


def is_staff_user(user):
    """Check if user is staff/admin"""
    return user.is_authenticated and user.is_staff


@require_http_methods(["GET"])
def admin_splashscreen(request):
    """Admin portal splashscreen view"""
    # If user is already authenticated and is staff, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('users:admin_dashboard')

    return render(request, 'admin/splashscreen.html')


@require_http_methods(["GET", "POST"])
def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('users:admin_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'admin/login.html')

        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_staff:
            login(request, user)

            # Set session expiry based on remember me
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes

            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('users:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')

    return render(request, 'admin/login.html')


@require_http_methods(["GET", "POST"])
def admin_signup(request):
    """Admin signup view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('users:admin_dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        agree_terms = request.POST.get('agree_terms')

        # Validation
        errors = []

        if not all([first_name, last_name, email, password1, password2]):
            errors.append('All fields are required.')

        if password1 != password2:
            errors.append('Passwords do not match.')

        if not agree_terms:
            errors.append('You must agree to the terms and conditions.')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('A user with this email already exists.')

        # Validate password strength
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors.extend(e.messages)

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'admin/signup.html')

        # Create user
        try:
            username = email.split('@')[0]  # Use email prefix as username
            # Ensure username is unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                is_staff=True  # Make admin user
            )

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('users:admin_login')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')

    return render(request, 'admin/signup.html')


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_dashboard(request):
    """Admin dashboard view with real data"""
    from datetime import datetime, timedelta
    from django.db.models import Count, Sum, Q, Avg
    from apps.leads.models import Booking, Client, Quotation
    from apps.services.models import Service
    from apps.portfolio.models import Project

    # Get current date for filtering
    today = datetime.now().date()
    this_month_start = today.replace(day=1)

    # Calculate statistics
    today_bookings = Booking.objects.filter(
        preferred_date=today
    ).count()

    active_services = Service.objects.filter(is_active=True).count()

    total_customers = Client.objects.count()

    # Calculate monthly revenue from completed bookings
    monthly_revenue = Booking.objects.filter(
        preferred_date__gte=this_month_start,
        status='completed',
        actual_cost__isnull=False
    ).aggregate(
        total=Sum('actual_cost')
    )['total'] or 0

    # Get recent bookings with proper status mapping
    recent_bookings_qs = Booking.objects.select_related(
        'service', 'client'
    ).order_by('-created_at')[:10]

    # Map status to Bootstrap classes
    status_class_map = {
        'new': 'primary',
        'confirmed': 'info',
        'in_progress': 'warning',
        'completed': 'success',
        'cancelled': 'danger',
        'rescheduled': 'secondary'
    }

    recent_bookings = []
    for booking in recent_bookings_qs:
        recent_bookings.append({
            'customer': booking.contact_name,
            'service': booking.service.name,
            'date': booking.preferred_date.strftime('%Y-%m-%d'),
            'status': booking.get_status_display(),
            'status_class': status_class_map.get(booking.status, 'secondary'),
            'booking_id': booking.booking_id.hex[:8]
        })

    # Additional statistics for dashboard cards
    pending_bookings = Booking.objects.filter(
        status__in=['new', 'confirmed']
    ).count()

    this_week_bookings = Booking.objects.filter(
        preferred_date__gte=today - timedelta(days=7),
        preferred_date__lte=today
    ).count()

    # Service performance analytics
    service_performance = Booking.objects.values(
        'service__name'
    ).annotate(
        total_bookings=Count('id'),
        completed_bookings=Count('id', filter=Q(status='completed')),
        total_revenue=Sum('actual_cost', filter=Q(status='completed')),
        avg_cost=Avg('actual_cost', filter=Q(status='completed'))
    ).order_by('-total_bookings')[:5]

    # Monthly booking trends (last 6 months)
    monthly_trends = []
    for i in range(6):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        month_bookings = Booking.objects.filter(
            created_at__date__gte=month_date,
            created_at__date__lt=month_date + timedelta(days=32)
        ).count()
        monthly_trends.append({
            'month': month_date.strftime('%b %Y'),
            'bookings': month_bookings
        })
    monthly_trends.reverse()

    # Status distribution
    status_distribution = Booking.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    # Portfolio statistics
    total_projects = Project.objects.count()
    published_projects = Project.objects.filter(is_published=True).count()
    featured_projects = Project.objects.filter(is_featured=True).count()
    draft_projects = Project.objects.filter(is_published=False).count()

    # Recent projects
    recent_projects = Project.objects.select_related().prefetch_related('images').order_by('-created_at')[:5]

    # Quotation statistics
    total_quotations = Quotation.objects.count()
    draft_quotations = Quotation.objects.filter(status='draft').count()
    sent_quotations = Quotation.objects.filter(status='sent').count()
    accepted_quotations = Quotation.objects.filter(status='accepted').count()
    pending_quotations = Quotation.objects.filter(status__in=['sent', 'viewed']).count()

    # Recent quotations
    recent_quotations = Quotation.objects.select_related('client', 'created_by').order_by('-created_at')[:5]

    # Quotation value statistics
    total_quotation_value = Quotation.objects.aggregate(
        total=Sum('total')
    )['total'] or 0

    accepted_quotation_value = Quotation.objects.filter(
        status='accepted'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    context = {
        'today_bookings': today_bookings,
        'active_services': active_services,
        'total_customers': total_customers,
        'monthly_revenue': int(monthly_revenue),
        'recent_bookings': recent_bookings,
        'pending_bookings': pending_bookings,
        'this_week_bookings': this_week_bookings,

        # Additional stats for future use
        'total_bookings': Booking.objects.count(),
        'completed_bookings': Booking.objects.filter(status='completed').count(),
        'active_quotations': Quotation.objects.filter(
            status__in=['sent', 'viewed']
        ).count(),

        # Analytics data
        'service_performance': service_performance,
        'monthly_trends': monthly_trends,
        'status_distribution': status_distribution,

        # Portfolio statistics
        'total_projects': total_projects,
        'published_projects': published_projects,
        'featured_projects': featured_projects,
        'draft_projects': draft_projects,
        'recent_projects': recent_projects,

        # Quotation statistics
        'total_quotations': total_quotations,
        'draft_quotations': draft_quotations,
        'sent_quotations': sent_quotations,
        'accepted_quotations': accepted_quotations,
        'pending_quotations': pending_quotations,
        'recent_quotations': recent_quotations,
        'total_quotation_value': int(total_quotation_value),
        'accepted_quotation_value': int(accepted_quotation_value),
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:admin_login')


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_bookings_list(request):
    """Admin bookings list view with filtering and search"""
    from django.db.models import Q
    from apps.leads.models import Booking

    # Get filter parameters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # Base queryset
    bookings = Booking.objects.select_related('service', 'client', 'assigned_technician').order_by('-created_at')

    # Apply filters
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    if priority_filter:
        bookings = bookings.filter(priority=priority_filter)

    if search_query:
        bookings = bookings.filter(
            Q(contact_name__icontains=search_query) |
            Q(contact_email__icontains=search_query) |
            Q(contact_phone__icontains=search_query) |
            Q(service__name__icontains=search_query) |
            Q(booking_id__icontains=search_query)
        )

    if date_from:
        bookings = bookings.filter(preferred_date__gte=date_from)

    if date_to:
        bookings = bookings.filter(preferred_date__lte=date_to)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter choices for dropdowns
    status_choices = Booking.STATUS_CHOICES
    priority_choices = Booking.PRIORITY_CHOICES

    context = {
        'bookings': page_obj,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
        'current_filters': {
            'status': status_filter,
            'priority': priority_filter,
            'search': search_query,
            'date_from': date_from,
            'date_to': date_to,
        },
        'total_bookings': bookings.count(),
    }

    return render(request, 'admin/bookings_list.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_booking_detail(request, booking_id):
    """Admin booking detail view with status management"""
    from apps.leads.models import Booking
    from django.contrib.auth.models import User

    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == 'POST':
        # Handle status updates
        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(Booking.STATUS_CHOICES):
                try:
                    booking.transition_status(new_status, user=request.user)
                    messages.success(request, f'Booking status updated to {booking.get_status_display()}')
                except ValueError as e:
                    messages.error(request, f'Invalid status transition: {e}')

        elif action == 'assign_technician':
            technician_id = request.POST.get('technician_id')
            if technician_id:
                try:
                    technician = User.objects.get(id=technician_id, is_staff=True)
                    booking.assigned_technician = technician
                    booking.save()
                    messages.success(request, f'Booking assigned to {technician.get_full_name() or technician.username}')
                except User.DoesNotExist:
                    messages.error(request, 'Invalid technician selected')

        elif action == 'update_notes':
            admin_notes = request.POST.get('admin_notes', '')
            booking.admin_notes = admin_notes
            booking.save()
            messages.success(request, 'Admin notes updated successfully')

        elif action == 'update_cost':
            try:
                estimated_cost = request.POST.get('estimated_cost')
                actual_cost = request.POST.get('actual_cost')

                if estimated_cost:
                    booking.estimated_cost = float(estimated_cost)
                if actual_cost:
                    booking.actual_cost = float(actual_cost)

                booking.save()
                messages.success(request, 'Cost information updated successfully')
            except (ValueError, TypeError):
                messages.error(request, 'Invalid cost values provided')

        return redirect('users:admin_booking_detail', booking_id=booking_id)

    # Get available technicians
    technicians = User.objects.filter(is_staff=True, is_active=True)

    context = {
        'booking': booking,
        'status_choices': Booking.STATUS_CHOICES,
        'priority_choices': Booking.PRIORITY_CHOICES,
        'technicians': technicians,
    }

    return render(request, 'admin/booking_detail.html', context)


def forgot_password(request):
    """Forgot password view - placeholder"""
    messages.info(request, 'Password reset functionality will be implemented soon.')
    return redirect('users:admin_login')


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_services_products(request):
    """Admin services and products management with tabbed interface"""
    from apps.services.models import Service, ServiceCategory, Product, ProductCategory
    from django.db.models import Count

    # Get services data
    services = Service.objects.select_related('category').order_by('-created_at')
    service_categories = ServiceCategory.objects.annotate(
        service_count=Count('services')
    ).order_by('order', 'name')

    # Get products data
    products = Product.objects.select_related('category').order_by('-created_at')
    product_categories = ProductCategory.objects.annotate(
        product_count=Count('products')
    ).order_by('order', 'name')

    # Get statistics
    total_services = services.count()
    active_services = services.filter(is_active=True).count()
    total_products = products.count()
    active_products = products.filter(is_active=True).count()
    total_categories = service_categories.count() + product_categories.count()

    context = {
        'services': services[:10],  # Latest 10 services
        'service_categories': service_categories,
        'products': products[:10],  # Latest 10 products
        'product_categories': product_categories,
        'total_services': total_services,
        'active_services': active_services,
        'total_products': total_products,
        'active_products': active_products,
        'total_categories': total_categories,
    }

    return render(request, 'admin/services_products.html', context)


# Service CRUD Views
@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_service_add(request):
    """Add new service"""
    from apps.services.forms import ServiceForm, ServiceImageFormSet
    from apps.services.models import Service
    from django.contrib import messages

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        image_formset = ServiceImageFormSet(request.POST, request.FILES)

        if form.is_valid() and image_formset.is_valid():
            service = form.save()
            image_formset.instance = service
            image_formset.save()
            messages.success(request, f'Service "{service.name}" has been created successfully.')
            return redirect('users:admin_services_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
        image_formset = ServiceImageFormSet()

    context = {
        'form': form,
        'image_formset': image_formset,
        'title': 'Add New Service',
        'action': 'Add'
    }
    return render(request, 'admin/service_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_service_view(request, service_id):
    """View service details"""
    from apps.services.models import Service
    from django.shortcuts import get_object_or_404

    service = get_object_or_404(Service, id=service_id)
    context = {
        'service': service,
        'title': f'View Service: {service.name}'
    }
    return render(request, 'admin/service_detail.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_service_edit(request, service_id):
    """Edit existing service"""
    from apps.services.forms import ServiceForm, ServiceImageFormSet
    from apps.services.models import Service
    from django.shortcuts import get_object_or_404
    from django.contrib import messages

    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        image_formset = ServiceImageFormSet(request.POST, request.FILES, instance=service)

        if form.is_valid() and image_formset.is_valid():
            service = form.save()
            image_formset.save()
            messages.success(request, f'Service "{service.name}" has been updated successfully.')
            return redirect('users:admin_services_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(instance=service)
        image_formset = ServiceImageFormSet(instance=service)

    context = {
        'form': form,
        'image_formset': image_formset,
        'service': service,
        'title': f'Edit Service: {service.name}',
        'action': 'Edit'
    }
    return render(request, 'admin/service_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_service_delete(request, service_id):
    """Delete service"""
    from apps.services.models import Service
    from django.shortcuts import get_object_or_404
    from django.contrib import messages

    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(request, f'Service "{service_name}" has been deleted successfully.')
        return redirect('users:admin_services_products')

    context = {
        'service': service,
        'title': f'Delete Service: {service.name}'
    }
    return render(request, 'admin/service_delete.html', context)


# Product CRUD Views
@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_product_add(request):
    """Add new product"""
    from apps.services.forms import ProductForm, ProductImageFormSet
    from apps.services.models import Product
    from django.contrib import messages

    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and image_formset.is_valid():
            product = form.save()
            image_formset.instance = product
            image_formset.save()
            messages.success(request, f'Product "{product.name}" has been created successfully.')
            return redirect('users:admin_services_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
        image_formset = ProductImageFormSet()

    context = {
        'form': form,
        'image_formset': image_formset,
        'title': 'Add New Product',
        'action': 'Add'
    }
    return render(request, 'admin/product_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_product_view(request, product_id):
    """View product details"""
    from apps.services.models import Product
    from django.shortcuts import get_object_or_404

    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'title': f'View Product: {product.name}'
    }
    return render(request, 'admin/product_detail.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_product_edit(request, product_id):
    """Edit existing product"""
    from apps.services.forms import ProductForm, ProductImageFormSet
    from apps.services.models import Product
    from django.shortcuts import get_object_or_404
    from django.contrib import messages

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and image_formset.is_valid():
            product = form.save()
            image_formset.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully.')
            return redirect('users:admin_services_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)

    context = {
        'form': form,
        'image_formset': image_formset,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'action': 'Edit'
    }
    return render(request, 'admin/product_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_product_delete(request, product_id):
    """Delete product"""
    from apps.services.models import Product
    from django.shortcuts import get_object_or_404
    from django.contrib import messages

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully.')
        return redirect('users:admin_services_products')

    context = {
        'product': product,
        'title': f'Delete Product: {product.name}'
    }
    return render(request, 'admin/product_delete.html', context)


# ============================================================================
# QUOTATION MANAGEMENT VIEWS
# ============================================================================

@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotations_list(request):
    """List all quotations with search and filtering"""
    from apps.leads.models import Quotation

    quotations = Quotation.objects.select_related('client', 'inquiry', 'created_by').all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        quotations = quotations.filter(
            Q(quote_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(client__name__icontains=search_query) |
            Q(client__email__icontains=search_query)
        )

    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        quotations = quotations.filter(status=status_filter)

    # Date filtering
    date_filter = request.GET.get('date_filter', '')
    if date_filter == 'today':
        quotations = quotations.filter(created_at__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timezone.timedelta(days=7)
        quotations = quotations.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = timezone.now() - timezone.timedelta(days=30)
        quotations = quotations.filter(created_at__gte=month_ago)

    # Ordering
    quotations = quotations.order_by('-created_at')

    # Pagination
    paginator = Paginator(quotations, 20)  # Show 20 quotations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics for dashboard
    stats = {
        'total_quotations': Quotation.objects.count(),
        'draft_quotations': Quotation.objects.filter(status='draft').count(),
        'sent_quotations': Quotation.objects.filter(status='sent').count(),
        'accepted_quotations': Quotation.objects.filter(status='accepted').count(),
        'pending_quotations': Quotation.objects.filter(status__in=['sent', 'viewed']).count(),
    }

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'stats': stats,
        'status_choices': Quotation.STATUS_CHOICES,
        'title': 'Quotation Management'
    }
    return render(request, 'admin/quotations_list.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotation_detail(request, quotation_id):
    """View quotation details"""
    from apps.leads.models import Quotation

    quotation = get_object_or_404(Quotation, id=quotation_id)

    context = {
        'quotation': quotation,
        'title': f'Quotation Details: {quotation.quote_number}'
    }
    return render(request, 'admin/quotation_detail.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotation_create(request):
    """Create new quotation"""
    from apps.leads.forms import QuotationForm
    from apps.leads.models import Quotation

    if request.method == 'POST':
        form = QuotationForm(request.POST)

        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.created_by = request.user

            # Quote number will be auto-generated in the model's save method
            quotation.save()
            messages.success(request, f'Quotation "{quotation.quote_number}" has been created successfully.')
            return redirect('users:admin_quotation_detail', quotation_id=quotation.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuotationForm()

    context = {
        'form': form,
        'title': 'Create New Quotation',
        'action': 'Create'
    }
    return render(request, 'admin/quotation_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotation_edit(request, quotation_id):
    """Edit existing quotation"""
    from apps.leads.forms import QuotationForm
    from apps.leads.models import Quotation

    quotation = get_object_or_404(Quotation, id=quotation_id)

    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=quotation)

        if form.is_valid():
            quotation = form.save()
            messages.success(request, f'Quotation "{quotation.quote_number}" has been updated successfully.')
            return redirect('users:admin_quotation_detail', quotation_id=quotation.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuotationForm(instance=quotation)

    context = {
        'form': form,
        'quotation': quotation,
        'title': f'Edit Quotation: {quotation.quote_number}',
        'action': 'Edit'
    }
    return render(request, 'admin/quotation_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotation_delete(request, quotation_id):
    """Delete quotation with confirmation"""
    from apps.leads.models import Quotation

    quotation = get_object_or_404(Quotation, id=quotation_id)

    if request.method == 'POST':
        quote_number = quotation.quote_number
        quotation.delete()
        messages.success(request, f'Quotation "{quote_number}" has been deleted successfully.')
        return redirect('users:admin_quotations_list')

    context = {
        'quotation': quotation,
        'title': f'Delete Quotation: {quotation.quote_number}'
    }
    return render(request, 'admin/quotation_delete.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_inquiry_to_quotation(request, inquiry_id):
    """Convert an inquiry to a quotation"""
    from apps.leads.models import Inquiry, Quotation, Client
    from datetime import date, timedelta
    import json

    inquiry = get_object_or_404(Inquiry, inquiry_id=inquiry_id)

    # Check if quotation already exists for this inquiry
    existing_quotation = Quotation.objects.filter(inquiry=inquiry).first()
    if existing_quotation:
        messages.warning(request, f'A quotation already exists for this inquiry: {existing_quotation.quote_number}')
        return redirect('users:admin_quotation_detail', quotation_id=existing_quotation.id)

    # Get or create client from inquiry
    client, created = Client.objects.get_or_create(
        email=inquiry.contact_email,
        defaults={
            'name': inquiry.contact_name,
            'phone': inquiry.contact_phone or '',
            'client_type': 'individual'
        }
    )

    if created:
        messages.info(request, f'New client created: {client.name}')

    # Create quotation from inquiry
    quotation = Quotation.objects.create(
        client=client,
        inquiry=inquiry,
        title=f'Quotation for {inquiry.subject}',
        description=inquiry.message,
        items=json.dumps([
            {
                'description': f'{inquiry.service.name if inquiry.service else "Service"} - Based on inquiry',
                'quantity': 1,
                'unit_price': 0.00,
                'total': 0.00
            }
        ]),
        subtotal=0.00,
        tax_rate=16.00,
        discount_amount=0.00,
        valid_until=date.today() + timedelta(days=30),
        terms_and_conditions='Terms and conditions to be finalized',
        created_by=request.user,
        notes=f'Created from inquiry {inquiry.inquiry_id.hex[:8].upper()}'
    )

    # Update inquiry status
    inquiry.status = 'in_progress'
    inquiry.save()

    messages.success(
        request,
        f'Quotation {quotation.quote_number} created successfully from inquiry. '
        f'Please update the line items and pricing details.'
    )

    return redirect('users:admin_quotation_edit', quotation_id=quotation.id)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotation_send_email(request, quotation_id):
    """Send quotation via email to client"""
    from apps.leads.models import Quotation
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.conf import settings

    quotation = get_object_or_404(Quotation, id=quotation_id)

    if request.method == 'POST':
        try:
            # Update quotation status to sent
            quotation.status = 'sent'
            quotation.sent_at = timezone.now()
            quotation.save()

            # Prepare email content
            subject = f'Quotation {quotation.quote_number} - Global Cool-Light E.A LTD'

            # Create email context
            context = {
                'quotation': quotation,
                'client': quotation.client,
                'company_name': 'Global Cool-Light E.A LTD',
                'company_email': settings.DEFAULT_FROM_EMAIL,
                'company_phone': '+254 700 000 000',  # Add to settings
            }

            # Render email template
            html_message = render_to_string('emails/quotation_email.html', context)
            plain_message = render_to_string('emails/quotation_email.txt', context)

            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quotation.client.email],
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(
                request,
                f'Quotation {quotation.quote_number} has been sent successfully to {quotation.client.email}'
            )

        except Exception as e:
            messages.error(request, f'Failed to send quotation: {str(e)}')

        return redirect('users:admin_quotation_detail', quotation_id=quotation.id)

    context = {
        'quotation': quotation,
    }
    return render(request, 'admin/quotation_send_email.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_quotation_status_update(request, quotation_id):
    """Update quotation status"""
    from apps.leads.models import Quotation

    quotation = get_object_or_404(Quotation, id=quotation_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Quotation.STATUS_CHOICES):
            old_status = quotation.get_status_display()
            quotation.status = new_status

            # Set timestamps based on status
            if new_status == 'sent' and not quotation.sent_at:
                quotation.sent_at = timezone.now()
            elif new_status in ['accepted', 'rejected'] and not quotation.decided_at:
                quotation.decided_at = timezone.now()

            quotation.save()

            messages.success(
                request,
                f'Quotation status updated from "{old_status}" to "{quotation.get_status_display()}"'
            )
        else:
            messages.error(request, 'Invalid status selected')

    return redirect('users:admin_quotation_detail', quotation_id=quotation.id)


# ============================================================================
# CUSTOMER MANAGEMENT VIEWS
# ============================================================================

@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_customers_list(request):
    """List all customers with search and filtering"""
    from apps.leads.models import Client
    from django.db.models import Count, Sum

    customers = Client.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(company_name__icontains=search_query)
        )

    # Client type filtering
    client_type_filter = request.GET.get('client_type', '')
    if client_type_filter:
        customers = customers.filter(client_type=client_type_filter)

    # Contact method filtering
    contact_method_filter = request.GET.get('contact_method', '')
    if contact_method_filter:
        customers = customers.filter(preferred_contact_method=contact_method_filter)

    # Date filtering
    date_filter = request.GET.get('date_filter', '')
    if date_filter == 'today':
        customers = customers.filter(created_at__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timezone.timedelta(days=7)
        customers = customers.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = timezone.now() - timezone.timedelta(days=30)
        customers = customers.filter(created_at__gte=month_ago)

    # Annotate with related data
    customers = customers.annotate(
        bookings_count=Count('bookings'),
        inquiries_count=Count('inquiries'),
        quotations_count=Count('quotations')
    )

    # Ordering
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', 'name', '-name', 'email', '-email',
                   '-total_bookings', 'total_bookings', '-total_spent', 'total_spent']
    if sort_by in valid_sorts:
        customers = customers.order_by(sort_by)
    else:
        customers = customers.order_by('-created_at')

    # Pagination
    paginator = Paginator(customers, 20)  # Show 20 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics for dashboard
    stats = {
        'total_customers': Client.objects.count(),
        'individual_customers': Client.objects.filter(client_type='individual').count(),
        'business_customers': Client.objects.filter(client_type='business').count(),
        'new_this_month': Client.objects.filter(
            created_at__gte=timezone.now().replace(day=1)
        ).count(),
        'total_revenue': Client.objects.aggregate(
            total=Sum('total_spent')
        )['total'] or 0,
    }

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'client_type_filter': client_type_filter,
        'contact_method_filter': contact_method_filter,
        'date_filter': date_filter,
        'sort_by': sort_by,
        'stats': stats,
        'client_type_choices': Client.CLIENT_TYPES,
        'contact_method_choices': Client.CONTACT_METHODS,
        'title': 'Customer Management'
    }
    return render(request, 'admin/customers_list.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_customer_add(request):
    """Add new customer"""
    from apps.leads.forms import ClientForm
    from apps.leads.models import Client

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer.name}" has been created successfully.')
            return redirect('users:admin_customer_view', customer_id=customer.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientForm()

    context = {
        'form': form,
        'title': 'Add New Customer',
        'action': 'Add'
    }
    return render(request, 'admin/customer_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_customer_view(request, customer_id):
    """View customer details"""
    from apps.leads.models import Client

    customer = get_object_or_404(Client, id=customer_id)

    # Get related data
    recent_bookings = customer.bookings.select_related('service').order_by('-created_at')[:5]
    recent_inquiries = customer.inquiries.select_related('service').order_by('-created_at')[:5]
    recent_quotations = customer.quotations.order_by('-created_at')[:5]

    # Calculate statistics
    stats = {
        'total_bookings': customer.bookings.count(),
        'completed_bookings': customer.bookings.filter(status='completed').count(),
        'total_inquiries': customer.inquiries.count(),
        'total_quotations': customer.quotations.count(),
        'accepted_quotations': customer.quotations.filter(status='accepted').count(),
        'total_spent': customer.total_spent,
        'avg_booking_value': customer.bookings.filter(
            actual_cost__isnull=False
        ).aggregate(avg=Avg('actual_cost'))['avg'] or 0,
    }

    context = {
        'customer': customer,
        'recent_bookings': recent_bookings,
        'recent_inquiries': recent_inquiries,
        'recent_quotations': recent_quotations,
        'stats': stats,
        'title': f'Customer Details: {customer.name}'
    }
    return render(request, 'admin/customer_detail.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_customer_edit(request, customer_id):
    """Edit existing customer"""
    from apps.leads.forms import ClientForm
    from apps.leads.models import Client

    customer = get_object_or_404(Client, id=customer_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=customer)

        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer.name}" has been updated successfully.')
            return redirect('users:admin_customer_view', customer_id=customer.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
        'title': f'Edit Customer: {customer.name}',
        'action': 'Edit'
    }
    return render(request, 'admin/customer_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_customer_delete(request, customer_id):
    """Delete customer with confirmation"""
    from apps.leads.models import Client

    customer = get_object_or_404(Client, id=customer_id)

    # Check if customer has related data
    has_bookings = customer.bookings.exists()
    has_inquiries = customer.inquiries.exists()
    has_quotations = customer.quotations.exists()

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            customer_name = customer.name
            customer.delete()
            messages.success(request, f'Customer "{customer_name}" has been deleted successfully.')
            return redirect('users:admin_customers_list')
        else:
            messages.info(request, 'Customer deletion cancelled.')
            return redirect('users:admin_customer_view', customer_id=customer.id)

    context = {
        'customer': customer,
        'has_bookings': has_bookings,
        'has_inquiries': has_inquiries,
        'has_quotations': has_quotations,
        'has_related_data': has_bookings or has_inquiries or has_quotations,
        'title': f'Delete Customer: {customer.name}'
    }
    return render(request, 'admin/customer_delete.html', context)


# ============================================================================
# SETTINGS VIEWS
# ============================================================================

@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_settings_general(request):
    """General settings page for site configuration"""
    from apps.core.models import SiteSettings
    from apps.core.forms import SiteSettingsForm

    # Get or create site settings
    site_settings, created = SiteSettings.objects.get_or_create(
        defaults={
            'company_name': 'Global Cool-Light E.A LTD',
            'tagline': 'Your Trusted HVAC Partner',
            'phone': '+254 700 000 000',
            'email': 'info@globalcool-light.com',
            'address': 'Nairobi, Kenya',
            'working_hours': 'Mon-Fri: 8AM-6PM, Sat: 9AM-4PM',
        }
    )

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'General settings have been updated successfully.')
            return redirect('users:admin_settings_general')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SiteSettingsForm(instance=site_settings)

    context = {
        'form': form,
        'site_settings': site_settings,
        'title': 'General Settings'
    }
    return render(request, 'admin/settings_general.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_account_settings(request):
    """User account settings page"""
    from .forms import UserProfileForm, UserAccountForm
    from django.contrib.auth.forms import PasswordChangeForm

    user_profile = request.user.profile

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            account_form = UserAccountForm(instance=request.user)
            password_form = PasswordChangeForm(request.user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile information updated successfully.')
                return redirect('users:admin_account_settings')
            else:
                messages.error(request, 'Please correct the errors in the profile form.')

        elif form_type == 'account':
            account_form = UserAccountForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(instance=user_profile)
            password_form = PasswordChangeForm(request.user)

            if account_form.is_valid():
                account_form.save()
                messages.success(request, 'Account information updated successfully.')
                return redirect('users:admin_account_settings')
            else:
                messages.error(request, 'Please correct the errors in the account form.')

        elif form_type == 'password':
            password_form = PasswordChangeForm(request.user, request.POST)
            profile_form = UserProfileForm(instance=user_profile)
            account_form = UserAccountForm(instance=request.user)

            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password changed successfully. Please log in again.')
                return redirect('users:admin_login')
            else:
                messages.error(request, 'Please correct the errors in the password form.')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        account_form = UserAccountForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'profile_form': profile_form,
        'account_form': account_form,
        'password_form': password_form,
        'user_profile': user_profile,
        'title': 'Account Settings'
    }
    return render(request, 'admin/settings_account.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_preferences(request):
    """User preferences settings page"""
    from .forms import UserPreferencesForm

    user_profile = request.user.profile

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferences updated successfully.')
            return redirect('users:admin_preferences')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPreferencesForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
        'title': 'User Preferences'
    }
    return render(request, 'admin/settings_preferences.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_user_management(request):
    """User management page for admin users"""
    from django.contrib.auth.models import User
    from django.db.models import Q

    # Get all staff users
    users = User.objects.filter(is_staff=True).select_related('profile').order_by('-date_joined')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Role filtering
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(profile__role=role_filter)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get role choices for filter dropdown
    from .models import UserProfile
    role_choices = UserProfile.ROLE_CHOICES

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': role_choices,
        'total_users': users.count(),
        'title': 'User Management'
    }
    return render(request, 'admin/settings_user_management.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_user_add(request):
    """Add new admin user"""
    from .forms import AdminUserCreationForm

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Admin user "{user.get_full_name() or user.username}" has been created successfully.')
            return redirect('users:admin_user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserCreationForm()

    context = {
        'form': form,
        'title': 'Add New Admin User',
        'action': 'Add'
    }
    return render(request, 'admin/settings_user_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_user_edit(request, user_id):
    """Edit existing admin user"""
    from .forms import AdminUserEditForm

    user = get_object_or_404(User, id=user_id, is_staff=True)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Admin user "{user.get_full_name() or user.username}" has been updated successfully.')
            return redirect('users:admin_user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserEditForm(instance=user)

    context = {
        'form': form,
        'user_obj': user,
        'title': f'Edit Admin User: {user.get_full_name() or user.username}',
        'action': 'Edit'
    }
    return render(request, 'admin/settings_user_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_user_delete(request, user_id):
    """Delete admin user with confirmation"""
    user = get_object_or_404(User, id=user_id, is_staff=True)

    # Prevent self-deletion
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('users:admin_user_management')

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            user_name = user.get_full_name() or user.username
            user.delete()
            messages.success(request, f'Admin user "{user_name}" has been deleted successfully.')
            return redirect('users:admin_user_management')
        else:
            messages.info(request, 'User deletion cancelled.')
            return redirect('users:admin_user_management')

    context = {
        'user_obj': user,
        'title': f'Delete Admin User: {user.get_full_name() or user.username}'
    }
    return render(request, 'admin/settings_user_delete.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_email_templates(request):
    """Email templates management page"""
    from apps.core.models import EmailTemplate
    from apps.core.forms import EmailTemplateForm

    # Get all email templates
    templates = EmailTemplate.objects.all().order_by('template_type', 'name')

    # Handle form submission for creating/editing templates
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        if template_id:
            # Edit existing template
            template = get_object_or_404(EmailTemplate, id=template_id)
            form = EmailTemplateForm(request.POST, instance=template)
        else:
            # Create new template
            form = EmailTemplateForm(request.POST)

        if form.is_valid():
            template = form.save()
            action = 'updated' if template_id else 'created'
            messages.success(request, f'Email template "{template.name}" has been {action} successfully.')
            return redirect('users:admin_email_templates')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmailTemplateForm()

    context = {
        'templates': templates,
        'form': form,
        'title': 'Email Templates Management'
    }
    return render(request, 'admin/settings_email_templates.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_security_settings(request):
    """Security settings page"""
    from apps.core.models import SecuritySettings
    from apps.core.forms import SecuritySettingsForm

    # Get or create security settings
    security_settings, created = SecuritySettings.objects.get_or_create(
        defaults={
            'session_timeout': 3600,  # 1 hour
            'max_login_attempts': 5,
            'password_min_length': 8,
            'password_require_uppercase': True,
            'password_require_lowercase': True,
            'password_require_numbers': True,
            'password_require_symbols': False,
        }
    )

    if request.method == 'POST':
        form = SecuritySettingsForm(request.POST, instance=security_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Security settings have been updated successfully.')
            return redirect('users:admin_security_settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SecuritySettingsForm(instance=security_settings)

    context = {
        'form': form,
        'security_settings': security_settings,
        'title': 'Security Settings'
    }
    return render(request, 'admin/settings_security.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_profile(request):
    """Admin profile page (referenced in sidebar)"""
    user_profile = request.user.profile

    context = {
        'user_profile': user_profile,
        'title': 'My Profile'
    }
    return render(request, 'admin/profile.html', context)


# ============================================================================
# LEADS MANAGEMENT VIEWS
# ============================================================================

@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_leads_list(request):
    """List all chat sessions (leads) with filtering and search"""
    from apps.leads.models import ChatSession
    from django.db.models import Q, Count, Max
    from django.core.paginator import Paginator

    # Base queryset with related data
    leads = ChatSession.objects.select_related('user').prefetch_related('messages').annotate(
        message_count=Count('messages'),
        last_message_time=Max('messages__timestamp'),
        unread_count=Count('messages', filter=Q(messages__is_read=False, messages__message_type='user'))
    ).order_by('-updated_at')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        leads = leads.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(session_id__icontains=search_query)
        )

    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        leads = leads.filter(is_active=True)
    elif status_filter == 'inactive':
        leads = leads.filter(is_active=False)
    elif status_filter == 'new':
        # New leads are those with messages but no admin responses
        leads = leads.filter(
            messages__isnull=False,
            is_active=True
        ).exclude(
            messages__message_type='agent'
        ).distinct()

    # Unread filter
    unread_filter = request.GET.get('unread', '')
    if unread_filter == 'true':
        leads = leads.filter(messages__is_read=False, messages__message_type='user').distinct()

    # Date filtering
    date_filter = request.GET.get('date', '')
    if date_filter:
        from datetime import datetime, timedelta
        today = datetime.now().date()

        if date_filter == 'today':
            leads = leads.filter(created_at__date=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            leads = leads.filter(created_at__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            leads = leads.filter(created_at__date__gte=month_ago)

    # Pagination
    paginator = Paginator(leads, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics
    total_leads = ChatSession.objects.count()
    active_leads = ChatSession.objects.filter(is_active=True).count()
    new_leads = ChatSession.objects.filter(
        messages__isnull=False,
        is_active=True
    ).exclude(
        messages__message_type='agent'
    ).distinct().count()
    unread_messages = ChatSession.objects.filter(
        messages__is_read=False,
        messages__message_type='user'
    ).distinct().count()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'unread_filter': unread_filter,
        'date_filter': date_filter,
        'total_leads': total_leads,
        'active_leads': active_leads,
        'new_leads': new_leads,
        'unread_messages': unread_messages,
        'title': 'Leads Management'
    }
    return render(request, 'admin/leads_list.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_lead_detail(request, session_id):
    """View detailed chat conversation for a specific lead"""
    from apps.leads.models import ChatSession, ChatMessage
    from django.http import JsonResponse

    # Get the chat session
    lead = get_object_or_404(ChatSession, session_id=session_id)

    # Get all messages for this session
    messages = ChatMessage.objects.filter(session=lead).order_by('timestamp')

    # Mark user messages as read
    ChatMessage.objects.filter(
        session=lead,
        message_type='user',
        is_read=False
    ).update(is_read=True)

    # Handle AJAX requests for real-time updates
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        last_message_id = request.GET.get('last_message_id', 0)
        new_messages = messages.filter(id__gt=last_message_id)

        message_data = []
        for message in new_messages:
            message_data.append({
                'id': message.id,
                'type': message.message_type,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_read': message.is_read
            })

        return JsonResponse({
            'success': True,
            'messages': message_data,
            'last_message_id': messages.last().id if messages.exists() else 0
        })

    context = {
        'lead': lead,
        'messages': messages,
        'title': f'Chat with {lead.name or "Anonymous"}'
    }
    return render(request, 'admin/lead_detail.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
@require_http_methods(["POST"])
def admin_lead_respond(request):
    """AJAX endpoint for admin to respond to chat messages"""
    from apps.leads.models import ChatSession, ChatMessage
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    import json

    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message_content = data.get('message', '').strip()

        if not session_id or not message_content:
            return JsonResponse({'error': 'Session ID and message content are required'}, status=400)

        # Get the chat session
        session = get_object_or_404(ChatSession, session_id=session_id)

        # Create admin message
        admin_message = ChatMessage.objects.create(
            session=session,
            message_type='agent',
            content=message_content,
            is_read=True  # Admin messages are automatically read
        )

        # Update session as active
        session.is_active = True
        session.save()

        return JsonResponse({
            'success': True,
            'message': {
                'id': admin_message.id,
                'content': admin_message.content,
                'timestamp': admin_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'type': admin_message.message_type
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
@require_http_methods(["POST"])
def admin_lead_status_update(request):
    """AJAX endpoint for updating chat session status"""
    from apps.leads.models import ChatSession
    from django.http import JsonResponse
    import json

    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        status = data.get('status')
        assigned_to_id = data.get('assigned_to')

        if not session_id:
            return JsonResponse({'error': 'Session ID is required'}, status=400)

        # Get the chat session
        session = get_object_or_404(ChatSession, session_id=session_id)

        # Update status if provided
        if status and status in ['active', 'closed', 'archived']:
            session.status = status
            if status == 'closed':
                session.is_active = False
            elif status == 'active':
                session.is_active = True

        # Update assigned user if provided
        if assigned_to_id:
            if assigned_to_id == 'unassign':
                session.assigned_to = None
            else:
                try:
                    assigned_user = User.objects.get(id=assigned_to_id, is_staff=True)
                    session.assigned_to = assigned_user
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Invalid assigned user'}, status=400)

        session.save()

        return JsonResponse({
            'success': True,
            'status': session.status,
            'assigned_to': session.assigned_to.get_full_name() if session.assigned_to else None
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
