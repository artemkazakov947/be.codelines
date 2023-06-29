from django.shortcuts import render
from django.views import generic

from apps.website.models import Employee


def contact_page(request):
    return render(request, "website/contact_page.html")


class OverOnsView(generic.ListView):
    model = Employee
    template_name = "website/over-ons.html"
    context_object_name = "employee_list"
    queryset = Employee.objects.all().select_related("role")
