from django.views.generic.base import ContextMixin

from apps.website.forms import RequestFromUserForm


class RequestFromUserMixin(ContextMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["form"] = RequestFromUserForm()
        return context


class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
