from urllib.request import Request

from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from taggit.models import Tag

from apps.website.forms import EmailPostNotificationForm, RequestFromUserForm
from apps.website.models import (
    Employee,
    Job,
    Post,
    Service,
    Case,
    WebApp,
    WebSite,
    MobileApp,
)
from base.decorators import request_from_user_form
from base.mixins import RequestFromUserMixin


def cookie(request):
    return render(request, "website/cookie.html")


def contact_page(request: Request):
    form = RequestFromUserForm
    context = {"form": form}
    return render(request, "website/contact_page.html", context=context)


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


class PostListView(RequestFromUserMixin, generic.ListView):
    model = Post
    queryset = Post.objects.all().prefetch_related("tag")
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["form_email"] = EmailPostNotificationForm()
        return context

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.GET.getlist("tags")
        if tags:
            queryset = queryset.filter(tag__name__in=tags)
        return queryset


class EmailForNotificationView(generic.FormView):
    form_class = EmailPostNotificationForm
    template_name = "website/post_list.html"
    success_url = reverse_lazy("website:post-list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class PostDetailView(RequestFromUserMixin, generic.DetailView):
    model = Post
    queryset = Post.objects.all().prefetch_related("tag")

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, pk=self.object.id)
        context = super().get_context_data(**kwargs)
        context["tagged_posts"] = (
            Post.objects.filter(tag__in=post.tag.all())
            .distinct()
            .prefetch_related("tag")
        )
        return context


class ServiceListView(RequestFromUserMixin, generic.ListView):
    model = Service
    queryset = Service.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["another_cases"] = Case.get_two_random_obj()
        return context


class RequestFromUserView(generic.FormView):
    form_class = RequestFromUserForm
    template_name = "includes/contact-section.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        referer_url = self.request.META.get("HTTP_REFERER")
        if referer_url:
            return referer_url
        return reverse_lazy("website:home")


class CaseListView(RequestFromUserMixin, generic.ListView):
    model = Case
    queryset = Case.objects.all()
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        return context


class CaseDetailView(generic.DetailView):
    model = Case
    queryset = Case.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["another_cases"] = Case.get_two_random_obj()
        return context


@request_from_user_form
def web_application(request: Request) -> TemplateResponse:
    webapp = WebApp.objects.all().prefetch_related("expectation").first()
    two_cases = Case.get_two_random_obj()
    context = {
        "name": webapp.name,
        "header_desc": webapp.header,
        "body_desc": webapp.description,
        "expectations": webapp.expectation.all(),
        "two_cases": two_cases,
    }
    return TemplateResponse(request, "website/web_application.html", context=context)


@request_from_user_form
def custom_website(request: Request) -> TemplateResponse:
    website: WebSite = WebSite.objects.all().prefetch_related("expectation").first()
    case_1 = Case.get_two_random_obj()[1]
    two_cases = Case.get_two_random_obj()
    context = {
        "name": website.name,
        "header_desc": website.header,
        "body_desc": website.description,
        "expectations": website.expectation.all(),
        "case_1": case_1,
        "two_cases": two_cases,
    }
    return TemplateResponse(request, "website/custom_website.html", context=context)


@request_from_user_form
def mobile_apps(request: Request) -> TemplateResponse:
    mobile_app: MobileApp = (
        MobileApp.objects.all().prefetch_related("expectation").first()
    )
    case_1 = Case.get_two_random_obj()[1]
    two_cases = Case.get_two_random_obj()
    context = {
        "name": mobile_app.name,
        "header_desc": mobile_app.header,
        "body_desc": mobile_app.description,
        "expectations": mobile_app.expectation.all(),
        "expect_desc": mobile_app.expect_desc,
        "case_1": case_1,
        "two_cases": two_cases,
    }
    return TemplateResponse(request, "website/mobile_apps.html", context=context)


@request_from_user_form
def home(request: Request) -> TemplateResponse:
    cases = Case.objects.all()
    two_cases = Case.get_two_random_obj()
    posts = Post.objects.all()
    context = {
        "cases": cases,
        "two_cases": two_cases,
        "posts": posts,
    }
    return TemplateResponse(request, "website/home.html", context=context)
