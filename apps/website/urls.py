from django.urls import path

from apps.website.views import (
    contact_page,
    OverOnsView,
    JobListView,
    JobDetailView,
    PostListView,
    PostDetailView,
)

urlpatterns = [
    path("contact/", contact_page, name="contact_page"),
    path("over-ons/", OverOnsView.as_view(), name="over-ons"),
    path("jobs/", JobListView.as_view(), name="job-list"),
    path("jobs/<slug:slug>/", JobDetailView.as_view(), name="job-detail"),
    path("blog/", PostListView.as_view(), name="post-list"),
    path("blog/<slug:slug>/", PostDetailView.as_view(), name="post-detail")
]
app_name = "website"
