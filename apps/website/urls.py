from django.urls import path

from apps.website.views import contact_page

urlpatterns = [
    path("contact/", contact_page, name="contact_page")
]
app_name = "website"
