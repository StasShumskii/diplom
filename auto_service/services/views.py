from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Service, ServiceCategory


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.objects.all()
        context["search_query"] = self.request.GET.get("search", "")
        context["category_id"] = self.request.GET.get("category", "")
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by category
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Search by name or description
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | queryset.filter(
                description__icontains=search_query
            )

        return queryset


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
