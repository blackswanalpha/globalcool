from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.urls import reverse
from .models import Project, ProjectImage, Testimonial
from .forms import ProjectForm, ProjectImageFormSet, TestimonialForm, PortfolioFilterForm


def is_staff_user(user):
    """Check if user is staff member"""
    return user.is_authenticated and user.is_staff


class PortfolioListView(ListView):
    model = Project
    template_name = 'portfolio/list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        queryset = Project.objects.filter(is_published=True).select_related().prefetch_related('images', 'services')

        # Apply filters
        project_type = self.request.GET.get('project_type')
        status = self.request.GET.get('status')
        featured_only = self.request.GET.get('featured_only')
        search = self.request.GET.get('search')

        if project_type:
            queryset = queryset.filter(project_type=project_type)

        if status:
            queryset = queryset.filter(status=status)

        if featured_only:
            queryset = queryset.filter(is_featured=True)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(client_name__icontains=search) |
                Q(location__icontains=search)
            )

        return queryset.order_by('-is_featured', '-end_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PortfolioFilterForm(self.request.GET)
        context['featured_projects'] = Project.objects.filter(
            is_published=True, is_featured=True
        ).prefetch_related('images')[:3]
        return context


class PortfolioDetailView(DetailView):
    model = Project
    template_name = 'portfolio/detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Project.objects.filter(is_published=True).select_related().prefetch_related(
            'images', 'services', 'testimonials'
        )

    def get_object(self):
        project = super().get_object()
        # Increment view count
        Project.objects.filter(pk=project.pk).update(view_count=F('view_count') + 1)
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get project images ordered by featured status and order
        context['project_images'] = self.object.images.all().order_by('-is_featured', 'order', 'created_at')

        # Get related projects (same type or services)
        related_projects = Project.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)

        if self.object.project_type:
            related_projects = related_projects.filter(project_type=self.object.project_type)

        context['related_projects'] = related_projects.prefetch_related('images')[:4]

        # Get testimonials for this project
        context['testimonials'] = self.object.testimonials.filter(is_published=True)

        return context


# Admin Views for Portfolio Management

@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_list(request):
    """Admin portfolio projects listing with search and filters"""
    projects = Project.objects.select_related().prefetch_related('images').order_by('-created_at')

    # Apply search
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(client_name__icontains=search) |
            Q(location__icontains=search)
        )

    # Apply filters
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)

    project_type = request.GET.get('project_type')
    if project_type:
        projects = projects.filter(project_type=project_type)

    is_published = request.GET.get('is_published')
    if is_published:
        projects = projects.filter(is_published=is_published == 'true')

    # Pagination
    paginator = Paginator(projects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': page_obj,
        'total_projects': projects.count(),
        'published_projects': Project.objects.filter(is_published=True).count(),
        'featured_projects': Project.objects.filter(is_featured=True).count(),
        'search_query': search,
        'current_status': status,
        'current_type': project_type,
        'current_published': is_published,
    }

    return render(request, 'admin/portfolio_list.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_add(request):
    """Add new portfolio project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        image_formset = ProjectImageFormSet(request.POST, request.FILES)

        if form.is_valid() and image_formset.is_valid():
            project = form.save()
            image_formset.instance = project
            image_formset.save()
            messages.success(request, f'Project "{project.title}" has been created successfully.')
            return redirect('users:admin_portfolio_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
        image_formset = ProjectImageFormSet()

    context = {
        'form': form,
        'image_formset': image_formset,
        'title': 'Add New Portfolio Project',
        'action': 'Add'
    }
    return render(request, 'admin/portfolio_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_edit(request, project_id):
    """Edit existing portfolio project"""
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        image_formset = ProjectImageFormSet(request.POST, request.FILES, instance=project)

        if form.is_valid() and image_formset.is_valid():
            project = form.save()
            image_formset.save()
            messages.success(request, f'Project "{project.title}" has been updated successfully.')
            return redirect('users:admin_portfolio_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)
        image_formset = ProjectImageFormSet(instance=project)

    context = {
        'form': form,
        'image_formset': image_formset,
        'project': project,
        'title': f'Edit Project: {project.title}',
        'action': 'Edit'
    }
    return render(request, 'admin/portfolio_form.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_detail(request, project_id):
    """View portfolio project details in admin"""
    project = get_object_or_404(Project, id=project_id)
    images = project.images.all().order_by('-is_featured', 'order', 'created_at')
    testimonials = project.testimonials.all().order_by('-is_featured', '-created_at')

    context = {
        'project': project,
        'images': images,
        'testimonials': testimonials,
    }
    return render(request, 'admin/portfolio_detail.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_delete(request, project_id):
    """Delete portfolio project"""
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Project "{project_title}" has been deleted successfully.')
        return redirect('users:admin_portfolio_list')

    context = {
        'project': project,
        'images_count': project.images.count(),
        'testimonials_count': project.testimonials.count(),
    }
    return render(request, 'admin/portfolio_delete.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_toggle_featured(request, project_id):
    """Toggle featured status of a project via AJAX"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.is_featured = not project.is_featured
        project.save()

        return JsonResponse({
            'success': True,
            'is_featured': project.is_featured,
            'message': f'Project "{project.title}" featured status updated.'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_portfolio_toggle_published(request, project_id):
    """Toggle published status of a project via AJAX"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.is_published = not project.is_published
        project.save()

        return JsonResponse({
            'success': True,
            'is_published': project.is_published,
            'message': f'Project "{project.title}" published status updated.'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Testimonial Management Views

@login_required
@user_passes_test(is_staff_user, login_url='users:admin_login')
def admin_testimonial_add(request):
    """Add new testimonial"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)

        if form.is_valid():
            testimonial = form.save()
            messages.success(request, f'Testimonial from "{testimonial.author_name}" has been created successfully.')
            return redirect('users:admin_portfolio_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestimonialForm()

    context = {
        'form': form,
        'title': 'Add New Testimonial',
        'action': 'Add'
    }
    return render(request, 'admin/testimonial_form.html', context)
