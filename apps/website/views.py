from django.shortcuts import render, get_object_or_404
from django.views import generic
from taggit.models import Tag

from apps.website.models import Employee, Job, Post


def contact_page(request):
    return render(request, "website/contact_page.html")


class OverOnsView(generic.ListView):
    model = Employee
    template_name = "website/over-ons.html"
    context_object_name = "employee_list"
    queryset = Employee.objects.all().select_related("role")


class JobListView(generic.ListView):
    model = Job
    queryset = Job.objects.all().prefetch_related("skill")


class JobDetailView(generic.DetailView):
    model = Job


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.all().prefetch_related("tag")
    paginate_by = 2
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.GET.getlist("tags")
        if tags:
            queryset = queryset.filter(tag__name__in=tags)
        return queryset


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        context["tagged_posts"] = Post.objects.filter(tag__in=post.tag.all()).distinct()
        return context
