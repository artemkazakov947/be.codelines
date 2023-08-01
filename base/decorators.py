from apps.website.forms import RequestFromUserForm


def request_from_user_form(view_func):
    def wrapper(request, *args, **kwargs):
        form = RequestFromUserForm()
        response = view_func(request, *args, **kwargs)
        response.context_data["form"] = form
        return response
    return wrapper
