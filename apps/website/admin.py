from django.contrib import admin
from apps.website.models import (
    Role,
    Employee,
    Skill,
    Job,
    Post,
    Service,
    EmailForPostNotification,
    Case,
    RequestFromUser,
    Expectation,
    WebApp,
    WebSite,
)
from base.mixins import BaseReadOnlyAdminMixin


admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Post)
admin.site.register(Service)
admin.site.register(EmailForPostNotification)
admin.site.register(Case)
admin.site.register(Expectation)
admin.site.register(WebApp)
admin.site.register(WebSite)


@admin.register(RequestFromUser)
class RequestFromUser(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("__str__",)
