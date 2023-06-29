from django.urls import path

from apps.website.views import (
    contact_page,
    OverOnsView,
)

urlpatterns = [
    path("contact/", contact_page, name="contact_page"),
    path("over-ons/", OverOnsView.as_view(), name="over-ons"),
]
app_name = "website"
