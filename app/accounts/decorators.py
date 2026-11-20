from functools import wraps

from django.shortcuts import redirect

from accounts.session import current_account


def signed_in_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if current_account(request) is None:
            return redirect("accounts:sign-in")
        return view(request, *args, **kwargs)

    return wrapper
