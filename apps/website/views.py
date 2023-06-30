from django.shortcuts import render
from django.views import generic

from apps.website.models import Employee, Job


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

