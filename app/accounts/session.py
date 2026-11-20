from accounts.models import Account

SESSION_KEY = "account_id"


def current_account(request):
    if not hasattr(request, "guestbook_account"):
        account = None
        account_id = request.session.get(SESSION_KEY)
        if account_id is not None:
            account = (
                Account.objects.exclude(status=Account.Status.CLOSED)
                .filter(pk=account_id)
                .first()
            )
            if account is None:
                request.session.pop(SESSION_KEY, None)
        request.guestbook_account = account
    return request.guestbook_account


def sign_in(request, account):
    request.session.cycle_key()
    request.session[SESSION_KEY] = account.pk
    request.guestbook_account = account


def sign_out(request):
    request.session.flush()
