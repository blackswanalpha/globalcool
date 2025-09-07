from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from .models import Service, ServiceCategory, Product, ProductCategory


class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related('category')

        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Featured services first
        return queryset.order_by('-is_featured', 'category__order', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(
            is_active=True,
            services__is_active=True
        ).distinct().order_by('order', 'name')
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search', '')

        # Add products to the context for combined services/products page
        context['products'] = Product.objects.filter(is_active=True).select_related('category')[:6]
        context['product_categories'] = ProductCategory.objects.filter(
            is_active=True,
            products__is_active=True
        ).distinct().order_by('order', 'name')

        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('category')

    def get_object(self):
        service = super().get_object()
        # Increment view count
        Service.objects.filter(pk=service.pk).update(view_count=F('view_count') + 1)
        return service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add related services from the same category
        context['related_services'] = Service.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]

        # Add booking URL with service pre-selected
        context['booking_url'] = f"/leads/booking/{self.object.slug}/"

        return context


class ProductListView(ListView):
    model = Product
    template_name = 'services/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')

        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Featured products first
        return queryset.order_by('-is_featured', 'category__order', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(
            is_active=True,
            products__is_active=True
        ).distinct().order_by('order', 'name')
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'services/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')

    def get_object(self):
        product = super().get_object()
        # Increment view count
        Product.objects.filter(pk=product.pk).update(view_count=F('view_count') + 1)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add related products from the same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]

        return context
