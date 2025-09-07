from django.shortcuts import render
from django.views.generic import ListView, DetailView


class BlogListView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Placeholder - will implement with actual Blog model
        return []


class BlogDetailView(DetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self):
        # Placeholder - will implement with actual Blog model
        return None
