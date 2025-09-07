from django.contrib import admin
from .models import Project, ProjectImage, Testimonial


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'title', 'image_type', 'is_featured', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'location', 'status', 'start_date', 'end_date', 'is_featured', 'is_published']
    list_filter = ['status', 'project_type', 'is_featured', 'is_published', 'start_date']
    search_fields = ['title', 'client_name', 'location', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    filter_horizontal = ['services']
    inlines = [ProjectImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'summary', 'description')
        }),
        ('Project Details', {
            'fields': ('client_name', 'location', 'project_type', 'services')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration_days', 'status', 'completion_percentage')
        }),
        ('Results', {
            'fields': ('results_metrics', 'challenges_solved'),
            'classes': ('collapse',)
        }),
        ('Visibility & SEO', {
            'fields': ('is_featured', 'is_published', 'meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'image_type', 'is_featured', 'order', 'created_at']
    list_filter = ['image_type', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'project__title']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'author_company', 'rating', 'is_published', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_published', 'is_featured', 'created_at']
    search_fields = ['author_name', 'author_company', 'quote']
    readonly_fields = ['created_at', 'updated_at']
