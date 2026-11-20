from django.utils.functional import SimpleLazyObject

from accounts.session import current_account


def account(request):
    return {"account": SimpleLazyObject(lambda: current_account(request))}
